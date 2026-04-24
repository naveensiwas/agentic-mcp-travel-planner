"""
Orchestrator Agent for the AI Travel Budget Planner.

This is a pure LLM agent (no tools). It receives the structured reports
produced by the Travel Research Agent and the Finance Agent, then synthesizes
them into a single, user-friendly travel plan.

Agent type : LLM-only (direct ainvoke — no ReAct loop, no tool calls)
LLM        : Groq (configured via config.settings.get_llm)
Input      : travel_report (str) + finance_report (str) from specialist agents
Output     : Formatted, human-readable travel plan with 7 sections
"""

from langchain_core.messages import HumanMessage
from config.settings import get_llm


async def run_orchestrator(
    destination: str,
    num_days: int,
    budget_usd: float,
    travel_report: str,
    finance_report: str,
) -> str:
    """Synthesize agent reports into a final, user-facing travel plan.

    No tools are used. The LLM is given a structured prompt containing
    trip details and both specialist reports, and asked to produce a
    concise, encouraging travel plan across 7 defined sections.

    Args:
        destination    (str):   Travel destination name (e.g., "Tokyo").
        num_days       (int):   Trip duration in days.
        budget_usd     (float): Total budget in USD.
        travel_report  (str):   Output from run_travel_agent() — weather,
                                tips, packing, and accommodation data.
        finance_report (str):   Output from run_finance_agent() — currency
                                conversion, daily budget, and verification.

    Returns:
        str: A complete, formatted travel plan covering:
             ✈️  Trip Overview
             🌤  Weather & Best Time to Visit
             🏨  Accommodation Estimate
             💵  Budget Breakdown
             🎒  Packing Essentials
             💡  Top 3 Local Tips
             ✅  Quick Checklist
    """
    print("\n🤖 Orchestrator Agent synthesizing the final travel plan...")

    llm = get_llm()

    # Structured prompt injects both specialist reports as context.
    # The 7-section output format keeps the final plan consistent and scannable.
    prompt = f"""You are a friendly AI travel planner. Based on the research below, create a 
concise and well-structured travel plan summary for the user.

TRIP DETAILS:
  - Destination : {destination}
  - Duration    : {num_days} days
  - Total Budget: ${budget_usd} USD

TRAVEL RESEARCH REPORT:
{travel_report}

FINANCE REPORT:
{finance_report}

Please produce a final travel plan that includes:
1. ✈️  Trip Overview
2. 🌤  Weather & Best Time to Visit
3. 🏨  Accommodation Estimate
4. 💵  Budget Breakdown (USD + local currency + daily spend)
5. 🎒  Packing Essentials
6. 💡  Top 3 Local Tips
7. ✅  Quick Checklist before you go

Keep it concise, practical, and encouraging!"""

    response = await llm.ainvoke([HumanMessage(content=prompt)])
    return response.content
