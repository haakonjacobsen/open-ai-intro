from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

def create_embedding(text: str) -> list[float]:
    """Returns the embedding from the OpenAI API"""
    # TODO: Implement the embedding function, test it by running the main script
    pass

if __name__ == "__main__":
    # Test the embedding function
    test_text = "Politiet stanset en bil for fartskontroll på Hamar"
    embedding = create_embedding(test_text)
    print(f"Embedding length: {len(embedding)}")
    print(f"First 5 values: {embedding[:5]}")