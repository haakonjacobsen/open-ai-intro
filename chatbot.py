import os
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

def chat_with_bot(user_input):
    """Send user input to OpenAI and return the response"""
    try:
        response = client.responses.create(
            model="gpt-4.1",
            input=user_input
        )
        return response
    except Exception as e:
        return f"Error: {str(e)}"

def main():
    """Main chatbot loop"""
    print("🤖 Simple OpenAI Chatbot")
    print("Type 'bye' or 'quit' to stop chatting\n")
    
    while True:
        # 1. Get user input
        user_input = input("🫵 User: ").strip()
        
        # 2. Check if user wants to quit
        if user_input.lower() in ['quit', 'exit', 'bye']:
            print("👋 Goodbye!")
            break
        
        # 3. Get bot response
        bot_response = chat_with_bot(user_input)
        print("🤖 Assistant:", bot_response.output_text)

if __name__ == "__main__":
    main()
