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
        )
        return response
    except Exception as e:
        return f"Error: {str(e)}"

def main():
    """Main chatbot loop"""
    print("🤖 Simple OpenAI Chatbot")
    print("Type 'bye' or 'quit' to stop chatting\n")

    messsages = []
    
    while True:
        # 1. Get user input
        user_input = input("🫵 User: ").strip()
        image_url = input("🖼️ Image URL (optional): ").strip()

        # 2. Check if user wants to quit
        if user_input.lower() in ['quit', 'exit', 'bye']:
            print("👋 Goodbye!")
            break

        if image_url:
            messsages.append(
            {
                "role": "user",
                "content": [
                    {"type": "input_text", "text": user_input},
                    {"type": "input_image", "image_url": image_url}
                ]
            })
        else:
            messsages.append({
                "role": "user",
                "content": user_input
            })

        # 3. Get bot response
        bot_response = chat_with_bot(messsages)
        print("🤖 Assistant:", bot_response.output_text)
        messsages.append({
            "role": "assistant",
            "content": bot_response.output_text
        })

if __name__ == "__main__":
    main()
