import html
import re

import httpx
from mcp.server.mcpserver import MCPServer
from mcp.server.mcpserver.exceptions import ToolError

# Example solution for Task 4: an MCP server for Store norske leksikon (SNL), the Norwegian encyclopedia
mcp = MCPServer("SNL")

HEADERS = {"User-Agent": "bekk-agent-workshop/1.0 github.com/bekk/open-ai-intro"}


def to_plain_text(markup: str) -> str:
    """SNL returns HTML. Strip the tags so the agent gets clean text."""
    text = re.sub(r"<[^>]+>", " ", markup)
    return re.sub(r"\s+", " ", html.unescape(text)).strip()


@mcp.tool()
async def search_snl(query: str) -> list[dict]:
    """Search Store norske leksikon (SNL), the Norwegian encyclopedia.

    Returns the best matching articles with a short snippet. Articles are in Norwegian.
    Use get_snl_article with the permalink to read the full article.
    """
    async with httpx.AsyncClient(headers=HEADERS) as client:
        response = await client.get(
            "https://snl.no/api/v1/search", params={"query": query, "limit": 5}
        )
        response.raise_for_status()

    return [
        {
            "title": article["title"],
            "permalink": article["permalink"],
            "snippet": to_plain_text(article["snippet"]),
            "url": article["article_url"],
        }
        for article in response.json()
    ]


@mcp.tool()
async def get_snl_article(permalink: str) -> str:
    """Get the full text of an SNL article, using the permalink from search_snl (e.g. 'Henrik_Ibsen')."""
    async with httpx.AsyncClient(headers=HEADERS) as client:
        response = await client.get(f"https://snl.no/{permalink}.json")

    if response.status_code == 404:
        # A ToolError is sent back to the agent as a failed tool call, with this message
        raise ToolError(f"No article with permalink '{permalink}'. Use search_snl to find it.")
    response.raise_for_status()

    article = response.json()
    # Long articles can be huge. Keep the start, which has the most important facts.
    return f"{article['title']}\n\n{to_plain_text(article['xhtml_body'])[:6000]}"


# Run the server on http://127.0.0.1:8001/mcp (the weather server already uses port 8000)
if __name__ == "__main__":
    mcp.run(transport="streamable-http", port=8001)
