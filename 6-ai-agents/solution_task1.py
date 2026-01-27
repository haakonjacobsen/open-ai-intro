import time

from dotenv import load_dotenv
from pydantic_ai import Agent, RunContext

# Load environment variables from .env file
load_dotenv()

database = {}

# Create a simple AI agent
agent = Agent(
    'openai:gpt-4o', # <- See that we prefix the model with the provider and model name <provider>:<model>
    system_prompt='You are a helpful assistant that can read and write data.',
)


@agent.tool
def read_data(ctx: RunContext[None], id: str) -> str:
    """Read data from the database by ID."""
    print(f"Reading data with id: {id}")
    if id in database:
        return f"Data for {id}: {database[id]}"
    return f"No data found for id: {id}"


@agent.tool
def write_data(ctx: RunContext[None], id: str, content: str) -> str:
    """Write data to the database by ID."""
    time.sleep(2)
    print(f"Writing '{content}' to id: {id}")
    database[id] = content
    return f"Successfully wrote '{content}' to {id}"


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
