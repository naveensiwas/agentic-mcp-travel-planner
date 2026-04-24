"""
MCP Weather Server
==================
A FastMCP server that provides weather conditions and climate classification
for popular travel destinations.

Tools provided:
  - get_weather(location)      -> Current weather conditions, temperature (degC/degF), and humidity
  - get_climate_type(location) -> Classifies a destination's climate: tropical / cold / temperate

Transport: streamable-http
  - Runs as a standalone HTTP server on http://localhost:8000/mcp
  - Must be started before running multi-agent or single-agent client scripts
  - MCP clients connect to it using the "streamable_http" transport type

Usage:
  Start the server:
    python servers/weather_server.py

  MCP client config (in multi_agent_multi_mcp_client.py / single_agent_multi_mcp_client.py):
    {
        "weather": {
            "url": "http://localhost:8000/mcp",
            "transport": "streamable_http"
        }
    }

Supported Locations (get_weather):
  Tokyo, Paris, New York, Bali, California

Supported Climate Classifications (get_climate_type):
  Tropical  -> Bali, Thailand, Singapore, Maldives
  Cold      -> Iceland, Norway, Canada, Alaska
  Temperate -> All other locations (default fallback)
"""

from mcp.server.fastmcp import FastMCP

# Initialise the FastMCP server with the name "Weather".
# This name identifies the server to any connected MCP client.
mcp = FastMCP("Weather")

# ─────────────────────────────────────────────
# Static weather dataset (mock data)
# In a real implementation, this would be replaced with
# a live API call (e.g. OpenWeatherMap, WeatherAPI).
# Keys are lowercase destination names for case-insensitive matching.
# ─────────────────────────────────────────────
WEATHER_DATA = {
    "tokyo":      {"condition": "Partly Cloudy", "temp_c": 18, "temp_f": 64, "humidity": "65%"},
    "paris":      {"condition": "Overcast",       "temp_c": 14, "temp_f": 57, "humidity": "72%"},
    "new york":   {"condition": "Sunny",          "temp_c": 22, "temp_f": 72, "humidity": "55%"},
    "bali":       {"condition": "Tropical Heat",  "temp_c": 31, "temp_f": 88, "humidity": "80%"},
    "california": {"condition": "Sunny",          "temp_c": 25, "temp_f": 77, "humidity": "45%"},
}


@mcp.tool()
async def get_weather(location: str) -> str:
    """Get current weather conditions and temperature for a travel destination.

    Performs a case-insensitive partial match against the known destinations,
    so inputs like "New York City" or "BALI" will still resolve correctly.

    Args:
        location (str): The name of the city or region to look up.

    Returns:
        str: A formatted string with condition, temperature (°C & °F), and humidity.
             Returns an error message if the location is not found in the dataset.

    Example:
        get_weather("Tokyo")
        → "🌤 Weather in Tokyo: Partly Cloudy, 18°C / 64°F, Humidity: 65%"
    """
    key = location.lower().strip()

    # Partial match in both directions:
    # e.g. "new york city" contains "new york", and "bali" is contained in "bali island"
    for dest, data in WEATHER_DATA.items():
        if dest in key or key in dest:
            return (
                f"🌤 Weather in {location.title()}: {data['condition']}, "
                f"{data['temp_c']}°C / {data['temp_f']}°F, Humidity: {data['humidity']}"
            )

    # Location not found in the static dataset
    return f"Weather data not available for '{location}'. Try: Tokyo, Paris, New York, Bali, California."


@mcp.tool()
async def get_climate_type(location: str) -> str:
    """Classify the general climate kind of destination.

    Used by the Travel Research Agent to determine what kind of
    packing list to recommend (via travel_tips_server.py).

    Classification logic:
      - Tropical  → hot and humid year-round (Bali, Thailand, Singapore, Maldives)
      - Cold      → sub-zero or freezing winters (Iceland, Norway, Canada, Alaska)
      - Temperate → mild, seasonal variation (default for all other destinations)

    Args:
        location (str): The name of the destination to classify.

    Returns:
        str: A sentence describing the climate type with a packing hint.

    Example:
        get_climate_type("Bali")
        → "Bali has a **tropical** climate — hot and humid year-round."
    """
    # Known tropical destinations — hot and humid year-round
    tropical = ["bali", "thailand", "singapore", "maldives"]

    # Known cold destinations — pack heavy winter clothing
    cold = ["iceland", "norway", "canada", "alaska"]

    key = location.lower()

    if any(t in key for t in tropical):
        return f"{location.title()} has a **tropical** climate — hot and humid year-round."
    elif any(c in key for c in cold):
        return f"{location.title()} has a **cold** climate — pack warm clothes."
    else:
        # Default fallback — temperate applies to most major cities (Tokyo, Paris, New York, etc.)
        return f"{location.title()} has a **temperate** climate — pack layers."


if __name__ == "__main__":
    # Start the MCP server using streamable-http transport.
    # FastMCP defaults to host=127.0.0.1 and port=8000.
    # The server will be accessible at: http://localhost:8000/mcp
    # Keep this process running in a dedicated terminal while using the app.
    mcp.run(transport="streamable-http")
