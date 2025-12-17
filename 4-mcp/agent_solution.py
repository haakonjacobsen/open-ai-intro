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
    instructions='You are a helpful assistant with access to calculator and utility tools. Use them when appropriate to answer questions.',
)


async def main():
    """Run the AI agent with various queries"""
    print("Starting AI Agent with MCP tools...\n")
    
    # Example 1: Basic math
    result = await agent.run('What is 42 plus 58?')
    print(f"Q: What is 42 plus 58?")
    print(f"A: {result.output}\n")
    
    # Example 2: Multiplication
    result = await agent.run('Can you multiply 7 by 8?')
    print(f"Q: Can you multiply 7 by 8?")
    print(f"A: {result.output}\n")
    
    # Example 3: String manipulation (if you added reverse_string tool)
    result = await agent.run('Can you reverse the string "Hello World"?')
    print(f"Q: Can you reverse the string "Hello World"?")
    print(f"A: {result.output}\n")
    
    # Example 4: Complex query
    result = await agent.run('Calculate 15 + 27, then multiply the result by 3')
    print(f"Q: Calculate 15 + 27, then multiply the result by 3")
    print(f"A: {result.output}\n")
    
    # Interactive mode
    print("=" * 50)
    print("Interactive mode - Type 'quit' to exit")
    print("=" * 50)
    
    while True:
        try:
            query = input("\nYou: ")
            if query.lower() in ['quit', 'exit', 'q']:
                print("Goodbye!")
                break
            
            result = await agent.run(query)
            print(f"Agent: {result.output}")
            
        except KeyboardInterrupt:
            print("\nGoodbye!")
            break
        except Exception as e:
            print(f"Error: {e}")


if __name__ == "__main__":
    # Check for API key
    if not os.getenv("OPENAI_API_KEY"):
        print("Error: Please set OPENAI_API_KEY in your .env file")
        print("Create a .env file with: OPENAI_API_KEY=your_api_key_here")
        exit(1)
    
    asyncio.run(main())

