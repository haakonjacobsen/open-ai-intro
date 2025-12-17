from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

def create_embedding(text: str) -> tuple[list[float], dict]:
    """Returns the embedding and the response from the OpenAI API"""
    try:
        response = client.embeddings.create(
            input=text,
            model="text-embedding-3-small",
        )
        embedding = response.data[0].embedding
        return embedding, response
    except Exception as e:
        print(f"Error creating embedding: {e}")
        return [], response