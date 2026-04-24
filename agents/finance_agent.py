"""
Finance Agent for the AI Travel Budget Planner.

This agent handles all budget and currency-related calculations for a trip.
It connects to two MCP servers:

  - currency server  (stdio) - usd_to_currency, get_daily_budget
  - math server      (stdio) - add, multiply

Agent type : Tool-calling agent via LangChain
LLM        : Groq (configured via config.settings.get_llm)
Transport  : stdio (both servers auto-spawned as subprocesses)
"""

from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain_core.messages import HumanMessage
from langchain.agents import create_agent
from config.settings import get_llm, get_server_configs


async def run_finance_agent(
    destination: str,
    budget_usd: float,
    num_days: int,
    local_currency: str,
) -> str:
    """Run the Finance Agent to calculate budget breakdown and currency conversion.

    Connects to the currency and math MCP servers, then invokes a tool-calling agent
    with the following sub-tasks:
      1. Convert total budget from USD to the destination's local currency.
      2. Calculate the daily budget in USD.
      3. Verify the total by multiplying daily budget x number of days.

    Args:
        destination    (str):   Name of the travel destination (e.g., "Tokyo").
        budget_usd     (float): Total travel budget in USD.
        num_days       (int):   Duration of the trip in days.
        local_currency (str):   ISO 4217 currency code for the destination
                                (e.g., "JPY", "EUR"). Sourced from CURRENCY_MAP.

    Returns:
        str: The agent's final response - a finance report covering USD/local
             conversion, daily allowance, and an arithmetic verification.
    """
    # Pull only the servers this agent needs (currency + math)
    all_configs = get_server_configs()
    servers = {
        "currency": all_configs["currency"],
        "math":     all_configs["math"],
    }

    # Initialise the MCP client and collect tools from both servers
    client = MultiServerMCPClient(servers)
    tools  = await client.get_tools()

    # Build a tool-calling agent with the aggregated tool set
    agent = create_agent(model=get_llm(), tools=tools)

    # Structured prompt asks for conversion, daily spend, and arithmetic verification
    query = (
        f"I have a total travel budget of ${budget_usd} USD for a {num_days}-day trip to {destination}. "
        f"Please: "
        f"(1) convert ${budget_usd} USD to {local_currency}, "
        f"(2) calculate my daily budget in USD using the daily budget tool, "
        f"(3) also tell me if I multiply daily budget by {num_days} what is the total "
        f"(use multiply tool to verify)."
    )

    result = await agent.ainvoke({"messages": [HumanMessage(content=query)]})

    # Return the last message which contains the agent's final answer
    return result["messages"][-1].content
