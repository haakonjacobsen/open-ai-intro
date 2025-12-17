import asyncio
import os
from dotenv import load_dotenv
from pydantic_ai import Agent
from pydantic_ai.mcp import MCPServerStreamableHTTP

# Load environment variables
load_dotenv()

# Connect to your local MCP server
mcp_server = MCPServerStreamableHTTP('http://127.0.0.1:8000/mcp')

# Create an AI agent with the MCP server tools
agent = Agent(
    'openai:gpt-4o',
    toolsets=[mcp_server],
    instructions='You are a helpful assistant with access to calculator tools.',
)


async def main():
    """Run the AI agent with a sample query"""
    print("Starting AI Agent with MCP tools...\n")
    
    # Example: Use the calculator tools from the MCP server
    result = await agent.run('What is 42 plus 58?')
    print(f"Agent response: {result.output}\n")
    
    # Another example
    result = await agent.run('Can you multiply 7 by 8?')
    print(f"Agent response: {result.output}\n")


if __name__ == "__main__":
    # Check for API key
    if not os.getenv("OPENAI_API_KEY"):
        print("Error: Please set OPENAI_API_KEY in your .env file")
        exit(1)
    
    asyncio.run(main())

