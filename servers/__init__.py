"""
Servers Package
===============
MCP server scripts for the AI Travel Budget Planner.

Each server exposes tools over the MCP protocol that are consumed
by the tool-calling agents in the agents/ package.

Servers:
  - math_server.py         : add, multiply            (stdio)
  - weather_server.py      : get_weather,              (streamable-http)
                             get_climate_type
  - currency_server.py     : usd_to_currency,          (stdio)
                             get_daily_budget
  - travel_tips_server.py  : get_destination_info,     (stdio)
                             get_packing_list,
                             estimate_accommodation_cost

Usage:
  weather_server must be started manually before running
  multi_agent_multi_mcp_client.py:
      python servers/weather_server.py

  All stdio servers are auto-spawned by MultiServerMCPClient.
"""
