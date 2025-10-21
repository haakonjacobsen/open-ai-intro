import json
import os
from pymongo import MongoClient
from bson import ObjectId
from dotenv import load_dotenv
from embedding import create_embedding

load_dotenv()

# Connect to MongoDB
mongo_uri = os.getenv('MONGODB_URI')
client = MongoClient(mongo_uri, serverSelectionTimeoutMS=5000, tlsAllowInvalidCertificates=True) # This TSL setting is a workaround, don't use it in production
db = client['<DATABASE_NAME>']
collection = db['<COLLECTION_NAME>']

def add_document(document: dict):
    """Add a document to the collection"""
    result = collection.insert_one(document)
    print(f"Document added with ID: {result.inserted_id}")
    return result

def update_document(document_id: str, fields_to_update: dict):
    """Update a document in the collection"""
    result = collection.update_one({'_id': ObjectId(document_id)}, {'$set': fields_to_update})
    print(f"Document with ID: {document_id} updated. Matched: {result.matched_count}, Modified: {result.modified_count}")
    return result

def semantic_search(query: str, limit: int = 5):
    """Search for relevant documents using vector search"""
    pass
    # TODO: Implement

# HELPER FUNCTIONS
def _add_documents_from_json(file_path: str):
    """Helper function to add documents from a JSON file to the collection"""
    with open(file_path, 'r') as file:
        documents = json.load(file)
    for document in documents:
        add_document(document)
    print(f"Documents added from {file_path}")

def _add_embeddings_to_documents():
    """Add embeddings to all documents in the collection"""
    documents = collection.find().limit(200) # Limit to 200 documents
    for document in documents:
        texts = document.get('messages', [])
        text = " ".join([item['text'] for item in texts])
        embedding, _ = create_embedding(text)
        doc = update_document(str(document['_id']), {'embedding': embedding})
        print(f"Document updated: {doc} with embedding length: {len(embedding)}")
        

if __name__ == "__main__":
    input("You are about to add the politiloggen.json data to your db. Press Enter to continue or Ctrl+C to exit.")
    #_add_documents_from_json('politiloggen.json')
    _add_embeddings_to_documents()

