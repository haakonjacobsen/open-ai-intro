import anthropic
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Initialize the Claude client. It reads ANTHROPIC_API_KEY from the environment.
client = anthropic.Anthropic()

# The model we send our requests to
MODEL = "claude-opus-5"

SYSTEM_PROMPT = "You are a helpful assistant that helps the user with their requests."


def chat_with_bot(messages):
    """Send the conversation to Claude and return the response"""
    response = client.messages.create(
        model=MODEL,
        max_tokens=4096,
        system=SYSTEM_PROMPT,
        messages=messages,
        # TODO: Add assistant tools
    )
    return response


def main():
    """Main assistant loop"""
    print("🤖 Simple Claude Assistant with Tools")
    print("Type 'bye' or 'quit' to stop assistant\n")

    messages = []

    while True:
        # 1. Get user input
        user_input = input("🫵 User: ").strip()

        # 2. Check if user wants to quit
        if user_input.lower() in ["quit", "exit", "bye"]:
            print("👋 Goodbye!")
            break

        # 3. Add user message to messages list
        messages.append({"role": "user", "content": user_input})

        # 4. Get assistant response
        response = chat_with_bot(messages)

        # 5. The reply is a list of content blocks. Pick out the text blocks and print them.
        assistant_text = "".join(block.text for block in response.content if block.type == "text")
        print("🤖 Assistant:", assistant_text)

        # 6. Add the full reply (all content blocks) to the conversation history
        messages.append({"role": "assistant", "content": response.content})


if __name__ == "__main__":
    main()
