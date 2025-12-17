from mcp.server.fastmcp import FastMCP
from datetime import datetime
import uuid

# Create an MCP server
mcp = FastMCP("Calculator")


@mcp.tool()
def add(a: int, b: int) -> int:
    """Add two numbers together and return the result"""
    return a + b


@mcp.tool()
def multiply(a: int, b: int) -> int:
    """Multiply two numbers together"""
    return a * b


@mcp.tool()
def reverse_string(text: str) -> str:
    """Reverse the characters in a string"""
    return text[::-1]


@mcp.tool()
def count_words(text: str) -> int:
    """Count the number of words in a text string"""
    return len(text.split())


@mcp.tool()
def generate_uuid() -> str:
    """Generate a random UUID (Universally Unique Identifier)"""
    return str(uuid.uuid4())


@mcp.tool()
def get_current_time(timezone: str = "UTC") -> str:
    """Get the current time. Timezone parameter is currently ignored, returns UTC time."""
    return datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")


@mcp.tool()
def calculate_percentage(part: float, whole: float) -> float:
    """Calculate what percentage 'part' is of 'whole'"""
    if whole == 0:
        return 0.0
    return (part / whole) * 100


# Run the server
if __name__ == "__main__":
    mcp.run(transport="streamable-http")

