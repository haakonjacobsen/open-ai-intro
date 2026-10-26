import os

from openai import OpenAI
from pymongo import MongoClient
from dotenv import load_dotenv
from embedding import create_embedding

load_dotenv()

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

# Connect to MongoDB
mongo_uri = os.getenv('MONGODB_URI')
client = MongoClient(mongo_uri, serverSelectionTimeoutMS=5000, tlsAllowInvalidCertificates=True) # This TSL setting is a workaround, don't use it in production
db = client['my-db']
threads_collection = db['logs']


def semantic_search(query: str, limit: int = 5):
    """Search for relevant documents using vector similarity"""
    # Create embedding for the question
    question_embedding, _ = create_embedding(query)
    if not question_embedding:
        print("Error creating embedding for question")
        return []
    
    # MongoDB vector search pipeline
    pipeline = [
        {
            "$vectorSearch": {
                "index": "default",
                "path": "embedding",
                "queryVector": question_embedding,
                "numCandidates": 100,
                "limit": limit
            }
        },
        {
            "$project": {
                "_id": 1,
                "messages": 1,
                "score": {"$meta": "vectorSearchScore"}
            }
        }
    ]
    
    # Execute search
    results = list(threads_collection.aggregate(pipeline))
    
    # Format results
    formatted_results = []
    for doc in results:
        content = '\n\n'.join([item['text'] for item in doc['messages']])
        formatted_results.append({
            'content': content,
            'id': str(doc['_id']),
            'score': doc.get('score', 0.0)
        })
    
    return formatted_results

if __name__ == "__main__":
    print("Semantic Search Tool")
    print("Type 'quit' to exit\n")
    
    while True:
        question = input("Enter your question: ").strip()
        if question.lower() == 'quit':
            break
        
        if not question:
            continue
            
        print(f"\nSearching for: '{question}'")
        print("-" * 50)
        
        results = semantic_search(question)
        
        if not results:
            print("No results found.")
        else:
            for i, result in enumerate(results, 1):
                print(f"\n{i}. Score: {result['score']:.4f}")
                print(f"Content: {result['content'][:200]}...")
                print(f"ID: {result['id']}")
        
        print("\n" + "="*50 + "\n")

