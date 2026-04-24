"""
Simple Single-Agent MCP Demo Client
===================================
A lightweight demo script that connects to two MCP servers, builds a single
LangChain tool-calling agent, and runs two example queries (math and weather).

This file is intended as a quick smoke-test / demonstration of the MCP
multiserver setup. For the full multi-agent travel planner, see
multi_agent_multi_mcp_client.py.

Agents:
  - 1 x LangChain tool-calling agent backed by a Groq LLM

MCP Servers used:
  - Math Server    (servers/math_server.py)    - stdio transport, auto-spawned
  - Weather Server (servers/weather_server.py) - streamable-http, start manually

Prerequisites:
  1. Start the weather server in a separate terminal:
       python servers/weather_server.py
  2. Ensure a .env file exists with:
       GROQ_API_KEY=<your_key>
       GROQ_MODEL=<model_name>   # optional, falls back to settings default

Usage:
  python single_agent_multi_mcp_client.py
"""

import asyncio
from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain.agents import create_agent
from config.settings import get_llm, get_server_configs


async def main():
    # ── 1. Load server configs (absolute paths from config/settings.py) ───────
    all_configs = get_server_configs()
    servers = {
        "math":    all_configs["math"],
        "weather": all_configs["weather"],
    }

    # ── 2. Initialise the multiserver MCP client ──────────────────────────────
    client = MultiServerMCPClient(servers)

    # ── 3. Fetch tools from all servers ───────────────────────────────────────
    try:
        tools = await client.get_tools()
    except Exception as exc:
        raise RuntimeError(
            "Failed to retrieve tools from MCP servers. "
            "Ensure servers/weather_server.py is running."
        ) from exc

    # ── 4. Build the ReAct agent ──────────────────────────────────────────────
    agent = create_agent(model=get_llm(), tools=tools)

    # ── 5. Run example queries ────────────────────────────────────────────────
    # Query 1: Math — agent should call add(23, 7) then multiply(30, 10) → 300
    math_response = await agent.ainvoke(
        {"messages": [{"role": "user", "content": "What's (23 + 7) x 10?"}]}
    )
    print("Math MCP response:", math_response["messages"][-1].content)

    # Query 2: Weather — agent should call get_weather("Paris")
    weather_response = await agent.ainvoke(
        {"messages": [{"role": "user", "content": "What is the weather in Paris?"}]}
    )
    print("Weather MCP response:", weather_response["messages"][-1].content)


if __name__ == "__main__":
    asyncio.run(main())
