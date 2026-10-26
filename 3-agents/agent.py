import asyncio

from claude_agent_sdk import (
    AssistantMessage,
    ClaudeAgentOptions,
    ClaudeSDKClient,
    ResultMessage,
    TextBlock,
    ToolUseBlock,
)
from dotenv import load_dotenv

# Load environment variables from .env file. The agent reads ANTHROPIC_API_KEY from the environment.
load_dotenv()

# The model the agent runs on
MODEL = "claude-opus-5-5"

# TODO (Task 1): Give your agent a job
SYSTEM_PROMPT = "You are a helpful assistant."

# Everything that defines the agent goes in the options
options = ClaudeAgentOptions(
    model=MODEL,
    system_prompt=SYSTEM_PROMPT,
    # The built-in tools the agent can see. An empty list means no built-in tools at all.
    # TODO (Task 1): Add built-in tools
    tools=[],
    # The tools the agent may run without asking. Every other tool call is denied.
    allowed_tools=[],
    # TODO (Task 2 and 3): Add your tools and MCP servers
    mcp_servers={},
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


async def main():
    """Main agent loop"""
    print("🤖 Claude Agent")
    print("Type 'bye' or 'quit' to stop the agent\n")

    # The client starts the agent and keeps the conversation going between questions
    async with ClaudeSDKClient(options=options) as client:
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
