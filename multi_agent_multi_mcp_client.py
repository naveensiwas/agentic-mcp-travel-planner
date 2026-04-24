"""
AI Travel Budget Planner (Entry Point)
======================================
Orchestrates the full multi-agent trip-planning pipeline.

Flow:
  1. Print trip banner                     (utils.display)
  2. Travel Research Agent -> travel_report (agents.travel_agent)
  3. Finance Agent         -> finance_report(agents.finance_agent)
  4. Orchestrator Agent    -> final_plan    (agents.orchestrator)
  5. Print finalised plan                  (utils.display)

Run:
  # Terminal 1 - start the weather HTTP server
  python servers/weather_server.py

  # Terminal 2 - run the planner
  python multi_agent_multi_mcp_client.py

Customise your trip by editing the asyncio.run() call at the bottom.

Environment (.env):
  GROQ_API_KEY  (required)
  GROQ_MODEL    (optional, defaults to configured value in settings)
"""

import asyncio
from agents import run_travel_agent, run_finance_agent, run_orchestrator
from config import CURRENCY_MAP
from utils  import print_banner, print_plan


async def plan_trip(destination: str, budget_usd: float, num_days: int) -> str:
    """Run the full multi-agent travel planning pipeline.

    Args:
        destination (str):   Target travel destination (e.g., "Tokyo").
        budget_usd  (float): Total trip budget in USD.
        num_days    (int):   Duration of the trip in days.

    Returns:
        str: The finalised, formatted travel plan from the Orchestrator Agent.
    """
    # ── 1. Display trip header ────────────────────────────────────────────────
    print_banner(destination, budget_usd, num_days)

    # ── 2. Resolve local currency (fallback: EUR) ─────────────────────────────
    # Used by the Finance Agent to select the correct conversion target.
    local_currency = CURRENCY_MAP.get(destination.lower(), "EUR")

    # ── 3. Run specialist agents sequentially ─────────────────────────────────
    # Sequential execution keeps subprocess/server interactions simpler and avoids
    # port or resource conflicts between the two stdio server groups.
    travel_report  = await run_travel_agent(destination, num_days)
    print("\n✅ Travel Research Agent completed. Report:")
    print(travel_report)

    finance_report = await run_finance_agent(destination, budget_usd, num_days, local_currency)
    print("\n✅ Finance Agent completed. Report:")
    print(finance_report)

    # ── 4. Synthesize reports into a final plan ───────────────────────────────
    final_plan = await run_orchestrator(
        destination, num_days, budget_usd, travel_report, finance_report
    )

    # ── 5. Display the final plan ─────────────────────────────────────────────
    print_plan(final_plan)

    return final_plan


if __name__ == "__main__":
    # ── Edit these values to plan a different trip ────────────────────────────
    asyncio.run(plan_trip(
        destination="Tokyo",
        budget_usd=3000,
        num_days=7,
    ))
