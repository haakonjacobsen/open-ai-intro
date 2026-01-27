import time
from dataclasses import dataclass
from datetime import date

from dotenv import load_dotenv
from pydantic import BaseModel, Field
from pydantic_ai import Agent, RunContext

from databaseService import Celebrity, CelebrityDatabase

# Load environment variables from .env file
load_dotenv()


@dataclass
class AgentDependencies:
    celebrity_db: CelebrityDatabase


class AgentCelebrityResponse(BaseModel):
    celebrity: str | None = Field(
        default=None,
        description="The name of the celebrity if one was found, otherwise None"
    )
    message: str = Field(
        description="A message from the AI describing the result"
    )


# Create agent with structured output
agent = Agent(
    'openai:gpt-4o',
    deps_type=AgentDependencies,
    output_type=AgentCelebrityResponse,
    system_prompt='You are a helpful assistant that manages a celebrity database.',
)


@agent.tool
def read_celebrity(ctx: RunContext[AgentDependencies], id: str) -> str:
    """Read a celebrity from the database by ID."""
    print(f"Reading celebrity with id: {id}")
    celebrity = ctx.deps.celebrity_db.read(id)
    if celebrity:
        return f"{celebrity.name}, {celebrity.profession}, born {celebrity.birthdate}"
    return f"No celebrity found for id: {id}"


@agent.tool
def write_celebrity(ctx: RunContext[AgentDependencies], name: str, profession: str, birthdate: date) -> str:
    """Write a celebrity to the database."""
    time.sleep(2)
    print(f"Writing {name}")
    id = ctx.deps.celebrity_db.write(Celebrity(name=name, profession=profession, birthdate=birthdate))
    return f"Successfully saved {name} with id {id}"


@agent.tool
def search_celebrity(ctx: RunContext[AgentDependencies], name: str) -> str:
    """Search for celebrities by name."""
    print(f"Searching for: {name}")
    results = ctx.deps.celebrity_db.search(name)
    if results:
        return "\n".join(f"ID {id}: {c.name}, {c.profession}" for id, c in results.items())
    return "No celebrities found"


def main():
    """Run the AI agent in a terminal chat loop."""
    print("AI Agent Chat")
    print("Type 'quit' to stop\n")

    deps = AgentDependencies(celebrity_db=CelebrityDatabase())

    while True:
        user_input = input("You: ").strip()

        if user_input.lower() in ['quit', 'exit', 'bye']:
            print("Goodbye!")
            break

        if not user_input:
            continue

        result = agent.run_sync(user_input, deps=deps)
        response = result.output
        if response.celebrity:
            print(f"Celebrity: {response.celebrity}")
        print(f"Agent: {response.message}\n")


if __name__ == "__main__":
    main()
