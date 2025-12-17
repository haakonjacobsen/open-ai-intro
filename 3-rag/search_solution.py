import os
import ssl

from openai import OpenAI
from pymongo import MongoClient
from dotenv import load_dotenv
from embedding_solution import create_embedding

load_dotenv()

# Initialize OpenAI client
openai_client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

# Connect to MongoDB
mongo_uri = os.getenv('MONGODB_URI')
mongo_client = MongoClient(
    mongo_uri, 
    serverSelectionTimeoutMS=5000, 
    tlsAllowInvalidCertificates=True,
    tlsInsecure=True,
    ssl_cert_reqs=ssl.CERT_NONE
) # These SSL/TLS settings are workarounds for development, don't use in production
db = mongo_client['my-db']
collection = db['logs']

def create_embedding(text: str) -> list[float]:
    """Returns the embedding and the response from the OpenAI API"""
    response = openai_client.embeddings.create(
        input=text,
        model="text-embedding-3-small",
    )
    embedding = response.data[0].embedding
    return embedding

def semantic_search(args: dict):
    """Search for relevant documents using vector similarity"""
    query = args.get('query')
    limit = args.get('limit', 5)
    print(f"Searching for: '{query}'")
    question_embedding = create_embedding(query)
    if not question_embedding:
        print("Error creating embedding for question")
        return []
    print(f"Embedding length: {len(question_embedding)}")
    print(f"First 5 values: {question_embedding[:5]}")
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
    results = list(collection.aggregate(pipeline))
    
    # Format results
    formatted_results = []
    for doc in results:
        print(doc)
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

