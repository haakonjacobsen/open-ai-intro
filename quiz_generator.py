import json
import os
from openai import OpenAI
from dotenv import load_dotenv
from pydantic import BaseModel

# Load environment variables from .env file
load_dotenv()

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

# The model for the quiz we want to generate
class Quiz(BaseModel):
    pass

def create_quiz(user_input):
    """Send user input to OpenAI and return the response"""
    try:
        response = client.responses.create(
            model="gpt-4.1",
            input=user_input
            # TO DO: Add the Quiz model as the response format
        )
        return response.output_text
    except Exception as e:
        return f"Error: {str(e)}"

def main():
    """Main chatbot loop"""
    # File path to genrate the quiz from
    file_path = input("🫵 Enter the file path to generate the quiz from: ")
    print(f"🤖 Generating quiz from {file_path}...")

    # Get the quiz from a text file
    with open(file_path, 'r') as f:
        content = f.read()

    # Create the quiz
    quiz = create_quiz(content)

    # Save the quiz to a JSON file
    with open('quiz.json', 'w') as f:
        json.dump(quiz, f)
    
    #TODO: Implement a way for users to play the quiz
    
if __name__ == "__main__":
    main()
