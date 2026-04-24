"""
MCP Server: Travel Tips
=======================
A FastMCP-based server that provides travel-related information and suggestions
for popular tourist destinations around the world.

Transport  : stdio (launched as a subprocess by MCP clients)
Framework  : FastMCP (from the `mcp` package)

Exposed Tools (callable by tool-calling agents via MCP protocol):
┌──────────────────────────────┬──────────────────────────────────────────────────────────┐
│ Tool                         │ Description                                              │
├──────────────────────────────┼──────────────────────────────────────────────────────────┤
│ get_destination_info         │ Returns country, language, currency, visa requirements,  │
│                              │ best travel season, and local tips for a destination.    │
├──────────────────────────────┼──────────────────────────────────────────────────────────┤
│ get_packing_list             │ Returns a suggested packing list based on climate type   │
│                              │ (tropical / cold / temperate).                           │
├──────────────────────────────┼──────────────────────────────────────────────────────────┤
│ estimate_accommodation_cost  │ Estimates nightly and total accommodation cost based on  │
│                              │ destination, number of days, and budget level.           │
└──────────────────────────────┴──────────────────────────────────────────────────────────┘

Supported Destinations : Tokyo, Paris, New York, Bali
Supported Climates     : tropical, cold, temperate
Budget Levels          : budget, mid-range, luxury

Usage:
  Automatically started by MultiServerMCPClient via stdio transport.
  Can also be run standalone for testing:
      python servers/travel_tips_server.py
"""

from mcp.server.fastmcp import FastMCP

# ─────────────────────────────────────────────
# Server Initialisation
# ─────────────────────────────────────────────
# Create a named FastMCP server instance.
# The name "TravelTips" identifies this server within the MCP client.
mcp = FastMCP("TravelTips")

# ─────────────────────────────────────────────
# Static Data: Destination Information
# ─────────────────────────────────────────────
# Lookup table keyed by lowercase destination name.
# Each entry holds essential travel facts and practical local tips
# that the tool-calling agent will surface in its travel report.
DESTINATION_INFO = {
    "tokyo": {
        "country": "Japan",
        "language": "Japanese",
        "currency": "JPY", # Used by Finance Agent for currency conversion
        "best_season": "March-May (Spring) or Oct-Nov (Autumn)",
        "visa": "Visa-free for most countries up to 90 days",
        "tips": [
            "Get a Suica/Pasmo IC card for public transport",
            "Cash is still widely used — carry yen",
            "Remove shoes when entering traditional restaurants or homes",
            "Download Google Translate with Japanese offline pack",
        ],
    },
    "paris": {
        "country": "France",
        "language": "French",
        "currency": "EUR",
        "best_season": "April-June or September-October",
        "visa": "Schengen visa required for non-EU travelers",
        "tips": [
            "Book major attractions (Eiffel Tower, Louvre) in advance",
            "Metro is the best way to get around",
            "Tipping is appreciated but not mandatory",
            "Learn a few basic French phrases — locals appreciate it",
        ],
    },
    "new york": {
        "country": "USA",
        "language": "English",
        "currency": "USD",
        "best_season": "April-June or September-November",
        "visa": "ESTA required for VWP countries",
        "tips": [
            "Get a MetroCard for subway and buses",
            "Tip 15-20% at restaurants",
            "Book Broadway shows in advance for better prices",
            "Walk across Brooklyn Bridge for great views",
        ],
    },
    "bali": {
        "country": "Indonesia",
        "language": "Balinese / Indonesian",
        "currency": "IDR",
        "best_season": "April-October (dry season)",
        "visa": "Visa on arrival for most nationalities",
        "tips": [
            "Rent a scooter for flexible travel",
            "Dress modestly when visiting temples",
            "Bargain at local markets",
            "Stay hydrated — tropical heat can be intense",
        ],
    },
}

# ─────────────────────────────────────────────
# Static Data: Packing Suggestions by Climate
# ─────────────────────────────────────────────
# Keyed by climate type (must match values returned by the weather server's
# get_climate_type tool so the agent can chain both tools seamlessly).
PACKING_SUGGESTIONS = {
    "tropical":  ["sunscreen", "light clothing", "insect repellent", "flip flops", "rain jacket"],
    "cold":      ["thermal layers", "heavy coat", "gloves", "scarf", "waterproof boots"],
    "temperate": ["layers", "comfortable walking shoes", "light jacket", "umbrella"],
}


# ─────────────────────────────────────────────
# Tool 1: get_destination_info
# ─────────────────────────────────────────────
@mcp.tool()
def get_destination_info(destination: str) -> str:
    """Get travel info for a destination: country, currency, visa, best season, and local tips.

    Args:
        destination (str): Name of the destination (e.g., "Tokyo", "Paris").

    Returns:
        str: Formatted travel summary including language, currency, visa requirements,
             best travel season, and a list of practical local tips.
             Returns an error message with available options if the destination is not found.
    """
    print(">>>> Travel tips server received request for destination info:", destination)
    # Normalise input to lowercase for case-insensitive lookup
    key = destination.lower().strip()

    # Return a helpful error listing supported destinations if not found
    if key not in DESTINATION_INFO:
        available = ", ".join(d.title() for d in DESTINATION_INFO)
        return f"Destination '{destination}' not found. Available: {available}"

    info = DESTINATION_INFO[key]

    # Format the tips list as a bullet-point string for readable LLM output
    tips_list = "\n  - ".join(info["tips"])

    return (
        f"📍 {destination.title()} ({info['country']})\n"
        f"  Language: {info['language']}\n"
        f"  Local Currency: {info['currency']}\n"
        f"  Best Season: {info['best_season']}\n"
        f"  Visa: {info['visa']}\n"
        f"  Travel Tips:\n  - {tips_list}"
    )


# ─────────────────────────────────────────────
# Tool 2: get_packing_list
# ─────────────────────────────────────────────
@mcp.tool()
def get_packing_list(climate: str) -> str:
    """Get a packing suggestion list based on climate type: tropical, cold, or temperate.

    Args:
        climate (str): Climate type — one of "tropical", "cold", or "temperate".
                       Typically derived from the weather server's get_climate_type tool.

    Returns:
        str: Comma-separated list of recommended packing items for the given climate.
             Returns an error message if the climate type is not recognised.
    """
    # Normalise input for case-insensitive lookup
    key = climate.lower().strip()

    if key not in PACKING_SUGGESTIONS:
        return f"Climate '{climate}' not recognized. Choose from: tropical, cold, temperate"

    items = ", ".join(PACKING_SUGGESTIONS[key])
    return f"Packing list for {climate} climate: {items}"


# ─────────────────────────────────────────────
# Tool 3: estimate_accommodation_cost
# ─────────────────────────────────────────────
@mcp.tool()
def estimate_accommodation_cost(destination: str, num_days: int, budget_level: str) -> str:
    """Estimate accommodation cost per night and total stay.

    Args:
        destination (str): Name of the destination (e.g., "Tokyo", "Bali").
        num_days    (int): Number of nights to stay.
        budget_level(str): Spending tier — "budget", "mid-range", or "luxury".

    Returns:
        str: A formatted string showing the per-night rate and total estimated cost in USD.
             Returns an error message if the destination or budget level is not found.
    """
    print(">>>> Travel tips server received request to estimate accommodation cost for:", destination, num_days, "nights at", budget_level, "level")
    # Per-night rates in USD, organised by destination and budget level
    costs = {
        "tokyo":    {"budget": 40,  "mid-range": 120, "luxury": 350},
        "paris":    {"budget": 50,  "mid-range": 150, "luxury": 400},
        "new york": {"budget": 80,  "mid-range": 200, "luxury": 500},
        "bali":     {"budget": 20,  "mid-range": 70,  "luxury": 200},
    }

    # Normalise both inputs for consistent lookup
    key   = destination.lower().strip()
    level = budget_level.lower().strip()

    if key not in costs:
        return f"Destination '{destination}' not in database."
    if level not in costs[key]:
        return f"Budget level must be: budget, mid-range, or luxury."

    per_night = costs[key][level]
    total     = per_night * num_days  # Simple multiplication — no hidden fees assumed

    return (
        f"Accommodation in {destination.title()} ({level}): "
        f"~${per_night}/night × {num_days} nights = ~${total} total"
    )


# ─────────────────────────────────────────────
# Entry Point
# ─────────────────────────────────────────────
if __name__ == "__main__":
    # Start the MCP server using stdio transport.
    # When launched by MultiServerMCPClient, stdin/stdout are used
    # as the communication channel between agent and server.
    mcp.run(transport="stdio")
