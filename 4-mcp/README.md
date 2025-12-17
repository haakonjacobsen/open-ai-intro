# MCP (Model Context Protocol) Workshop

## What is MCP?

Remember function calling from the earlier workshops? **MCP (Model Context Protocol)** takes that concept to the next level! 🚀

Instead of defining tools directly in your application code, MCP lets you host them on a **remote server**. Any AI client can then pull these tools from the server and use them - think of it as **"Capabilities as a Service"** for AI applications, just like an API but specifically designed for LLMs.

**MCP servers can provide three main features:**

- 🛠️ **Tools**: Functions that LLMs can call to perform actions (focus of today's workshop!)
- 📚 **Resources**: Data and content that LLMs can access
- 💬 **Prompts**: Reusable prompt templates for common interactions

## How to Run

1. **Install uv** (if you don't have it):

   ```bash
   # macOS/Linux
   curl -LsSf https://astral.sh/uv/install.sh | sh
   ```

   ```bash
   # Windows
   powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
   ```

2. **Navigate to the workshop folder**:

   ```bash
   cd 4-mcp
   ```

3. **Install dependencies**:

   ```bash
   uv sync
   ```

   This will create a virtual environment and install the required packages.

4. **Create a `.env` file** (needed for Task 4):

   ```
   OPENAI_API_KEY=your_openai_api_key_here
   ```

## Workshop Tasks

### Task 1: Run Your First MCP Server

Time to see MCP in action! We'll run a simple calculator server and test it. 🧮

**Your Mission:**
Run the MCP server and test it with the MCP Inspector.

**What You'll Learn:**

- How to structure an MCP server
- How to define tools that AI models can call
- How to test your server with MCP Inspector

**Steps:**

1. **Examine the Server Code**

   Open `main.py` and notice the structure:

```python
from mcp.server.fastmcp import FastMCP

# Create an MCP server
mcp = FastMCP("Calculator")

@mcp.tool()
def add(a: int, b: int) -> int:
    """Add two numbers together and return the result"""
    return a + b
```

**Key Points:**

- `FastMCP("Calculator")` creates your server
- `@mcp.tool()` decorator exposes functions as tools
- The docstring helps AI understand what the tool does
- Type hints (`int`, etc.) define the tool's parameters

2. **Run Your Server**

   Start your MCP server:

   ```bash
   uv run main.py
   ```

   You should see: `Uvicorn running on http://127.0.0.1:8000` which is the MCP server.

3. **Test with MCP Inspector**

   In a **separate terminal**, open the MCP Inspector:

   ```bash
   npx -y @modelcontextprotocol/inspector
   ```

   - Connect to `http://127.0.0.1:8000/mcp` (remember the /mcp)
   - You should see your `add` tool listed
   - Try calling it with values like `a=5, b=3`

**Success Check:**

- ✅ Server starts without errors
- ✅ Inspector shows your `add` tool
- ✅ You can call the tool and get results (e.g., 5 + 3 = 8)

**What Just Happened?**
You created a tool that any AI client can now discover and use! The MCP server exposes the `add` function, and AI models can call it to perform calculations. 🎉

### Task 2: Add More Tools to Your MCP Server

Now let's make your MCP server more powerful by adding useful tools! 🛠️

**Your Mission:**
Add some more tools to your MCP server, e.g. reuse tools from previous workshops or create new ones.

**From Previous Workshops:**

- `semantic_search(query: str)` - Search through police logs (from RAG workshop). This would require you to add dependencies for mongoose (MongoDB) to this pyproject.
- `send_slack_message(message: str)` - Send notifications (from functions workshop)
- Any other tools you created in earlier workshops!

2. **Restart Your Server**

   Stop the server (Ctrl+C) and restart it:

   ```bash
   uv run main.py
   ```

3. **Test in Inspector**

   Refresh the MCP Inspector and you should see all your new tools listed! Try calling each one to make sure they work.

**Tips:**

- Always include clear docstrings - they become the tool descriptions for the AI
- Use type hints or Pydantic classes for all parameters and return values

### Task 3: Connect to Cursor

Now try to connect your MCP server to an AI Application like Cursor, Copilot, Claude etc.

The type of server we've created is of type Streamable HTTP, which means it's available from a remote URL, in our case `http://127.0.0.1:8000/mcp`.

### Task 4: Create an AI Agent with Pydantic AI

Time to build an AI agent that uses your MCP tools! We'll use Pydantic AI to create an agent that connects to your MCP server. 🤖

**What is Pydantic AI?**
Pydantic AI is a Python framework for building production-grade AI agents. It supports MCP out of the box, making it easy to connect agents to MCP servers.

**Steps:**

1. **Create a `.env` file** with your OpenAI API key:

   ```
   OPENAI_API_KEY=your_api_key_here
   ```

2. **Update dependencies**:

   ```bash
   uv sync
   ```

3. **Examine the agent code**

   Open `agent.py` and notice how it connects to the MCP server:

```python
from pydantic_ai import Agent
from pydantic_ai.mcp import MCPServerStreamableHTTP

# Connect to your local MCP server
mcp_server = MCPServerStreamableHTTP('http://127.0.0.1:8000/mcp')

# Create an AI agent with the MCP server tools
agent = Agent(
    'openai:gpt-4o',
    toolsets=[mcp_server],
    instructions='You are a helpful assistant with access to calculator tools.',
)
```

**Key Points:**

- `MCPServerStreamableHTTP` connects to your MCP server
- `toolsets=[mcp_server]` gives the agent access to all your MCP tools
- The agent automatically discovers and uses available tools

4. **Run the agent**

   Make sure your MCP server is running in one terminal:

   ```bash
   uv run main.py
   ```

   Then in another terminal, run the agent:

   ```bash
   uv run agent.py
   ```

**Success Check:**

- ✅ Agent connects to MCP server
- ✅ Agent uses your tools to answer questions
- ✅ You see the agent's responses

**Try Your Own Queries:**
Modify the queries in `agent.py` to test your tools!

**Learn More:** [Pydantic AI MCP Documentation](https://ai.pydantic.dev/integrations/mcp/)

## Congratulations! 🎉

You've built a complete MCP workflow:

- ✅ Created an MCP server with tools
- ✅ Connected it to AI applications
- ✅ Built an AI agent that uses MCP tools

**What's Next?**

- Add more complex tools (database queries, API calls)
- Connect your RAG tools from workshop 3
- Explore Pydantic AI's other features

Learn more: [modelcontextprotocol.io](https://modelcontextprotocol.io/) | [ai.pydantic.dev](https://ai.pydantic.dev/)
