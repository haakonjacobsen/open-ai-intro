import time
from dataclasses import dataclass
from datetime import date

import httpx
from dotenv import load_dotenv
from pydantic import BaseModel, Field
from pydantic_ai import Agent, RunContext

from databaseService import Celebrity, CelebrityDatabase

# Load environment variables from .env file
load_dotenv()


@dataclass
class AgentDependencies:
    celebrity_db: CelebrityDatabase
    http_client: httpx.Client


class AgentCelebrityResponse(BaseModel):
    celebrity: str | None = Field(
        default=None,
        description="The name of the celebrity if one was found, otherwise None"
    )
    message: str = Field(
        description="A message from the AI describing the result"
    )


SYSTEM_PROMPT = f"""You are a helpful assistant that manages a celebrity database.
Todays date is {date.today().strftime("%Y-%m-%d")}.

IMPORTANT: You must ONLY write verified data to the database.
- Before adding or updating a celebrity, use snl_search and snl_fetch to verify the information
- Never trust user-provided birthdates or professions without verification
- If you cannot verify the data, refuse to write it
"""

# Create agent with structured output
agent = Agent(
    'openai:gpt-4o',
    deps_type=AgentDependencies,
    output_type=AgentCelebrityResponse,
    system_prompt=SYSTEM_PROMPT,
)


@agent.tool
def snl_search(ctx: RunContext[AgentDependencies], query: str) -> str:
    """Search Store norske leksikon (SNL) for articles."""
    import snl
    print(f"Searching SNL for: {query}")
    results = snl.search(query, limit=3, client=ctx.deps.http_client)
    if not results:
        return f"No results found for {query}"
    return str(results)


@agent.tool
def snl_fetch(ctx: RunContext[AgentDependencies], permalink: str) -> str:
    """Fetch full article from SNL by permalink (e.g. 'Taylor_Swift')."""
    import snl
    print(f"Fetching SNL article: {permalink}")
    return snl.fetch(permalink, client=ctx.deps.http_client)


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
    """Write a verified celebrity to the database. Only use after verifying with snl_search/snl_fetch."""
    time.sleep(2)
    print(f"Writing {name}")
    id = ctx.deps.celebrity_db.write(Celebrity(name=name, profession=profession, birthdate=birthdate))
    return f"Successfully saved {name} with id {id}"


@agent.tool
def search_celebrity(ctx: RunContext[AgentDependencies], name: str) -> str:
    """Search for celebrities by name in the database."""
    print(f"Searching for: {name}")
    results = ctx.deps.celebrity_db.search(name)
    if results:
        return "\n".join(f"ID {id}: {c.name}, {c.profession}" for id, c in results.items())
    return "No celebrities found"


def main():
    """Run the AI agent in a terminal chat loop."""
    print("AI Agent Chat")
    print("Type 'quit' to stop\n")

    deps = AgentDependencies(
        celebrity_db=CelebrityDatabase(),
        http_client=httpx.Client()
    )

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
