import asyncio
from typing import Any

from claude_agent_sdk import (
    AssistantMessage,
    ClaudeAgentOptions,
    ClaudeSDKClient,
    ResultMessage,
    TextBlock,
    ToolUseBlock,
    create_sdk_mcp_server,
    tool,
)
from dotenv import load_dotenv

# Load environment variables from .env file. The agent reads ANTHROPIC_API_KEY from the environment.
load_dotenv()

# The model the agent runs on
MODEL = "claude-opus-5-5"

# Task 1: Give the agent a job
SYSTEM_PROMPT = """You are a personal assistant for a consultant in Norway.
You help them plan their day: what to do, what to wear, and what to keep track of.
Use your tools to look things up instead of guessing, and keep your answers short.
Answer in the same language as the user."""


# Task 2: Tools that belong to this agent only.
# They read and write the todo list in this Python process, which no other agent can see.
todos: list[str] = []


@tool("add_todo", "Add an item to the user's todo list", {"item": str})
async def add_todo(args: dict[str, Any]) -> dict[str, Any]:
    todos.append(args["item"])
    return {"content": [{"type": "text", "text": f"Added '{args['item']}' ({len(todos)} items)"}]}


@tool("list_todos", "List everything on the user's todo list", {})
async def list_todos(args: dict[str, Any]) -> dict[str, Any]:
    if not todos:
        return {"content": [{"type": "text", "text": "The todo list is empty"}]}
    lines = [f"{number}. {item}" for number, item in enumerate(todos, start=1)]
    return {"content": [{"type": "text", "text": "\n".join(lines)}]}


@tool(
    "complete_todo",
    "Remove an item from the todo list by its number in list_todos",
    {"number": int},
)
async def complete_todo(args: dict[str, Any]) -> dict[str, Any]:
    index = args["number"] - 1
    if not 0 <= index < len(todos):
        # is_error tells the agent the call failed, so it can try again
        return {
            "content": [{"type": "text", "text": f"No item number {args['number']}"}],
            "is_error": True,
        }
    item = todos.pop(index)
    return {"content": [{"type": "text", "text": f"Completed '{item}'"}]}


# Custom tools are wrapped in an in-process MCP server that only this agent can see
todo_server = create_sdk_mcp_server(name="todo", tools=[add_todo, list_todos, complete_todo])


options = ClaudeAgentOptions(
    model=MODEL,
    system_prompt=SYSTEM_PROMPT,
    # Task 1: Built-in tools from Claude Code
    tools=["WebSearch", "WebFetch"],
    allowed_tools=[
        "WebSearch",
        "WebFetch",
        "mcp__todo__*",  # Task 2: our own tools
        "mcp__weather__*",  # Task 3: the weather MCP server
        "mcp__deepwiki__*",  # Task 3: a public MCP server someone else runs
        "mcp__snl__*",  # Task 4: our own MCP server
    ],
    mcp_servers={
        # Task 2: In-process, lives and dies with this agent
        "todo": todo_server,
        # Task 3: Separate services that any MCP client can connect to.
        # Start them first with `python weather_server.py` and `python solution_server.py`.
        "weather": {"type": "http", "url": "http://127.0.0.1:8000/mcp"},
        "deepwiki": {"type": "http", "url": "https://mcp.deepwiki.com/mcp"},
        # Task 4: Our own MCP server
        "snl": {"type": "http", "url": "http://127.0.0.1:8001/mcp"},
    },
    # Start from a clean slate: don't load your personal Claude Code settings or MCP servers
    setting_sources=[],
    strict_mcp_config=True,
)


def print_message(message):
    """Print what the agent is doing: its replies, the tools it calls, and what the turn cost"""
    if isinstance(message, AssistantMessage):
        for block in message.content:
            if isinstance(block, TextBlock):
                print("🤖 Agent:", block.text)
            elif isinstance(block, ToolUseBlock):
                print(f"🔧 Calling tool: {block.name} with arguments: {block.input}")

    elif isinstance(message, ResultMessage):
        # The last message of every turn, with stats for the whole turn
        if message.is_error:
            print(f"❌ The agent stopped with an error: {message.subtype}")
        print(f"📊 {message.num_turns} turn(s), ${message.total_cost_usd or 0:.4f}\n")


async def print_mcp_status(client):
    """Show which MCP servers the agent managed to connect to"""
    # Remote servers connect in the background, so give them a few seconds
    for _ in range(10):
        servers = (await client.get_mcp_status())["mcpServers"]
        if all(server["status"] != "pending" for server in servers):
            break
        await asyncio.sleep(1)

    for server in servers:
        icon = "✅" if server["status"] == "connected" else "⚠️ "
        print(f"{icon} MCP server '{server['name']}': {server['status']}")
    print()


async def main():
    """Main agent loop"""
    print("🤖 Claude Agent")
    print("Type 'bye' or 'quit' to stop the agent\n")

    # The client starts the agent and keeps the conversation going between questions
    async with ClaudeSDKClient(options=options) as client:
        await print_mcp_status(client)

        while True:
            # 1. Get user input (in a thread, so we don't block the agent while waiting)
            user_input = (await asyncio.to_thread(input, "🫵 User: ")).strip()

            # 2. Check if user wants to quit
            if user_input.lower() in ["quit", "exit", "bye"]:
                print("👋 Goodbye!")
                break
            if not user_input:
                continue

            # 3. Send the message. The agent runs its loop: thinking, calling tools, answering.
            await client.query(user_input)

            # 4. Print everything the agent does until it's done with this turn
            async for message in client.receive_response():
                print_message(message)


if __name__ == "__main__":
    asyncio.run(main())
