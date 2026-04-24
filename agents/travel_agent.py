"""
Travel Research Agent for the AI Travel Budget Planner.

This agent is responsible for gathering all destination-related information
needed to plan a trip. It connects to two MCP servers:

  - weather server       (HTTP)  - get_weather, get_climate_type
  - travel_tips server   (stdio) - get_destination_info, get_packing_list,
                                   estimate_accommodation_cost

Agent type : Tool-calling agent via LangChain
LLM        : Groq (configured via config.settings.get_llm)
Transport  : weather -> streamable_http | travel_tips -> stdio
"""

from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain_core.messages import HumanMessage
from langchain.agents import create_agent

from config.settings import get_llm, get_server_configs


async def run_travel_agent(destination: str, num_days: int) -> str:
    """Run the Travel Research Agent for a given destination and duration.

    Connects to the weather and travel_tips MCP servers, then invokes a
    tool-calling agent with the following sub-tasks:
      1. Fetch current weather conditions.
      2. Retrieve destination info and local travel tips.
      3. Get a climate-appropriate packing list.
      4. Estimate mid-range accommodation cost for the stay.

    Args:
        destination (str): Name of the travel destination (e.g., "Tokyo").
        num_days    (int): Duration of the trip in days.

    Returns:
        str: The agent's final response - a structured travel research report
             covering weather, tips, packing, and accommodation.
    """
    # Pull only the servers this agent needs (weather + travel_tips)
    all_configs = get_server_configs()
    servers = {
        "weather":     all_configs["weather"],
        "travel_tips": all_configs["travel_tips"],
    }

    # Initialise the MCP client and collect tools from both servers
    client = MultiServerMCPClient(servers)
    tools  = await client.get_tools()

    # Build a tool-calling agent with the aggregated tool set
    agent = create_agent(model=get_llm(), tools=tools)

    # Structured prompt ensures all four data points are always collected,
    # making the downstream orchestrator's synthesis more predictable.
    query = (
        f"I am planning a {num_days}-day trip to {destination}. "
        f"Please: "
        f"(1) get the current weather, "
        f"(2) get destination travel info and tips, "
        f"(3) get a packing list based on the climate, "
        f"(4) estimate mid-range accommodation cost for {num_days} days."
    )

    result = await agent.ainvoke({"messages": [HumanMessage(content=query)]})

    # Return the last message which contains the agent's final answer
    return result["messages"][-1].content
