from dotenv import load_dotenv
from pydantic_ai import Agent

# Load environment variables from .env file
load_dotenv()

database = {}

# Create a simple AI agent
agent = Agent(
    'openai:gpt-4o',
    system_prompt='You are a helpful assistant that can read and write data.',
)


# Task 1: Add your tools here


def main():
    """Run the AI agent in a terminal chat loop."""
    print("AI Agent Chat")
    print("Type 'quit' to stop\n")

    while True:
        user_input = input("You: ").strip()

        if user_input.lower() in ['quit', 'exit', 'bye']:
            print("Goodbye!")
            break

        if not user_input:
            continue

        result = agent.run_sync(user_input)
        print(f"Agent: {result.output}\n")


if __name__ == "__main__":
    main()
