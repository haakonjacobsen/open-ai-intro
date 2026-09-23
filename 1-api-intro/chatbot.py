import anthropic
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Initialize the Claude client. It reads ANTHROPIC_API_KEY from the environment.
client = anthropic.Anthropic()

# The model we send our requests to
MODEL = "claude-opus-5"


def chat_with_bot(user_input):
    """Send user input to Claude and return the response"""
    response = client.messages.create(
        model=MODEL,
        max_tokens=4096,
        messages=[{"role": "user", "content": user_input}],
    )
    return response


def main():
    """Main chatbot loop"""
    print("🤖 Simple Claude Chatbot")
    print("Type 'bye' or 'quit' to stop chatting\n")

    while True:
        # 1. Get user input
        user_input = input("🫵 User: ").strip()

        # 2. Check if user wants to quit
        if user_input.lower() in ["quit", "exit", "bye"]:
            print("👋 Goodbye!")
            break

        # 3. Get bot response
        response = chat_with_bot(user_input)

        # 4. The reply is a list of content blocks. Pick out the text blocks and print them.
        assistant_text = "".join(block.text for block in response.content if block.type == "text")
        print("🤖 Assistant:", assistant_text)


if __name__ == "__main__":
    main()
