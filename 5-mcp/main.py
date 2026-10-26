from mcp.server.fastmcp import FastMCP

# Create an MCP server
mcp = FastMCP("Calculator") # <- The name can be anything

"""
Adding the @mcp.tool() decorator makes the function available as a tool to the AI.
The decorator will automatically check the function arguments and return type, and add them to the tool info.
The docstring is automatically detected and used as the tool description.
"""
@mcp.tool()
def add(a: int, b: int) -> int:
    """Add two numbers together and return the result"""
    return a + b


# Run the server
if __name__ == "__main__":
    mcp.run(transport="streamable-http")

