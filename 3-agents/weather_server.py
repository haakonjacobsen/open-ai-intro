import httpx
from mcp.server.mcpserver import MCPServer
from mcp.server.mcpserver.exceptions import ToolError

# Create an MCP server. Any MCP client can connect to it: your agent, Claude Code, Cursor, ...
mcp = MCPServer("Weather")

# MET Norway requires an identifying User-Agent: https://api.met.no/doc/TermsOfService
HEADERS = {"User-Agent": "bekk-agent-workshop/1.0 github.com/bekk/open-ai-intro"}

"""
Adding the @mcp.tool() decorator makes the function available as a tool.
The function name becomes the tool name, the docstring becomes the description,
and the type hints become the input schema. That's all the agent gets to see,
so write them for the model.
"""


@mcp.tool()
async def find_place(name: str) -> list[dict]:
    """Find places in Norway by name (cities, neighbourhoods, mountains, lakes, ...).

    Returns the matching places with their latitude and longitude.
    Use this to get the coordinates for get_forecast.
    """
    async with httpx.AsyncClient(headers=HEADERS) as client:
        response = await client.get(
            "https://ws.geonorge.no/stedsnavn/v1/navn",
            params={"sok": name, "treffPerSide": 5, "utkoordsys": 4258},
        )
        response.raise_for_status()

    places = response.json()["navn"]
    if not places:
        # A ToolError is sent back to the agent as a failed tool call, with this message
        raise ToolError(f"No places in Norway named '{name}'. Check the spelling.")

    # Only return the fields the agent needs
    return [
        {
            "name": place["skrivemåte"],
            "type": place["navneobjekttype"],
            "municipality": ", ".join(k["kommunenavn"] for k in place["kommuner"]),
            "latitude": place["representasjonspunkt"]["nord"],
            "longitude": place["representasjonspunkt"]["øst"],
        }
        for place in places
    ]


@mcp.tool()
async def get_forecast(latitude: float, longitude: float, hours: int = 24) -> list[dict]:
    """Get the hour-by-hour weather forecast from MET Norway (yr.no) for a location.

    Covers up to 48 hours ahead. Times are in UTC, temperature is in °C,
    wind speed in m/s and precipitation in mm for the next hour.
    """
    async with httpx.AsyncClient(headers=HEADERS) as client:
        response = await client.get(
            "https://api.met.no/weatherapi/locationforecast/2.0/compact",
            # MET asks for at most 4 decimals in the coordinates
            params={"lat": round(latitude, 4), "lon": round(longitude, 4)},
        )
        response.raise_for_status()

    # The full response has ~80 time steps with lots of fields. Trim it so it
    # doesn't fill up the agent's context window.
    forecast = []
    for step in response.json()["properties"]["timeseries"][: min(hours, 48)]:
        now = step["data"]["instant"]["details"]
        next_hour = step["data"].get("next_1_hours", {})
        forecast.append(
            {
                "time": step["time"],
                "temperature": now["air_temperature"],
                "wind_speed": now["wind_speed"],
                "precipitation": next_hour.get("details", {}).get("precipitation_amount"),
                "weather": next_hour.get("summary", {}).get("symbol_code"),
            }
        )
    return forecast


# Run the server on http://127.0.0.1:8000/mcp
if __name__ == "__main__":
    mcp.run(transport="streamable-http", port=8000)
