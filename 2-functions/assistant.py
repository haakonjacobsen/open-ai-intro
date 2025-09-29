import os
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))


def chat_with_bot(messages):
    """Send user input to OpenAI and return the response"""
    try:
        response = client.responses.create(
            model="gpt-4.1",
            input=messages,
            #TODO: Add assistant tools
        )
        return response
    except Exception as e:
        return f"Error: {str(e)}"

def main():
    """Main chatbot loop"""
    print("🤖 Simple OpenAI Assistant with Tools")
    print("Type 'bye' or 'quit' to stop assistant\n")

    messsages = []
    
    while True:
        # 1. Get user input
        user_input = input("🫵 User: ").strip()

        # 2. Check if user wants to quit
        if user_input.lower() in ['quit', 'exit', 'bye']:
            print("👋 Goodbye!")
            break
        
        # 3. Add user message to messages list
        messsages.append({
            "role": "user",
            "content": user_input
        })

        # 4. Get assistant response
        bot_response = chat_with_bot(messsages)
        print("🤖 Assistant:", bot_response.output_text)
        messsages.append({
            "role": "assistant",
            "content": bot_response.output_text
        })

if __name__ == "__main__":
    main()
