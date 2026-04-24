"""
MCP Currency & Budget Server
============================
A FastMCP server that exposes simple finance tools for AI agents.
It is designed for local demo use (fixed rates, no external API calls).

Tools provided:
  - usd_to_currency(amount, currency): Convert USD to a supported currency
  - get_daily_budget(total_budget, num_days): Compute daily spend limit

Transport: stdio
  - The server reads tool requests from stdin and writes responses to stdout.
  - Intended to be spawned by an MCP client process (e.g. MultiServerMCPClient).

Usage:
  python currency_server.py

Example MCP client config:
  {
    "currency": {
      "command": "python",
      "args": ["currency_server.py"],
      "transport": "stdio"
    }
  }
"""

from mcp.server.fastmcp import FastMCP

# Register this MCP server under the logical name "Currency".
mcp = FastMCP("Currency")

# Static conversion rates relative to 1 USD.
# Note: These are demo values and can drift from real-world exchange rates.
RATES = {
    "EUR": 0.92,
    "INR": 83.5,
    "GBP": 0.79,
    "JPY": 149.5,
    "CAD": 1.36,
    "AUD": 1.53,
}


@mcp.tool()
def usd_to_currency(amount: float, currency: str) -> str:
    """Convert USD to one supported target currency.

    Args:
        amount (float): USD amount to convert.
        currency (str): Target code (EUR, INR, GBP, JPY, CAD, AUD).

    Returns:
        str: A formatted conversion result or a supported-currencies message.
    """
    print(">>>> Currency Server received request to convert:", amount, "USD to", currency)
    normalized_currency = currency.upper().strip()

    if normalized_currency not in RATES:
        supported = ", ".join(RATES.keys())
        return f"Currency '{normalized_currency}' not supported. Supported: {supported}"

    converted = round(amount * RATES[normalized_currency], 2)
    return f"${amount} USD = {converted} {normalized_currency} (rate: {RATES[normalized_currency]})"


@mcp.tool()
def get_daily_budget(total_budget: float, num_days: int) -> str:
    """Calculate a per-day budget from a total budget and trip duration.

    Args:
        total_budget (float): Total available budget in USD.
        num_days (int): Number of travel days.

    Returns:
        str: Daily budget summary, or validation message for invalid days.
    """
    print(">>>> Daily Budget Server received request to calculate daily budget for:", total_budget, "USD over", num_days, "days")
    if num_days <= 0:
        return "Number of days must be greater than 0."

    daily = round(total_budget / num_days, 2)
    return f"Total budget: ${total_budget} | Days: {num_days} | Daily budget: ${daily}/day"


if __name__ == "__main__":
    # Start server over stdio for subprocess-based MCP integration.
    mcp.run(transport="stdio")
