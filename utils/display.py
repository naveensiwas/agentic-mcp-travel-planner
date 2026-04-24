"""
Console display helpers for the AI Travel Budget Planner.

Provides consistent, emoji-enhanced banner and plan output functions
so that all print formatting lives in one place rather than being
scattered across agent modules.

Functions:
  - print_banner(destination, budget_usd, num_days) : Prints the trip header.
  - print_plan(plan)                                : Prints the final travel plan.
"""

# Width of the separator lines used throughout the console output
DIVIDER_WIDTH = 60
DIVIDER       = "=" * DIVIDER_WIDTH


def print_banner(destination: str, budget_usd: float, num_days: int) -> None:
    """Print the trip overview banner at the start of a planning run.

    Args:
        destination (str):   Name of the travel destination.
        budget_usd  (float): Total budget in USD.
        num_days    (int):   Duration of the trip in days.

    Example output:
        ============================================================
          🌍 AI Travel Budget Planner
          Destination : Tokyo
          Budget      : $3000 USD
          Duration    : 7 days
        ============================================================
    """
    print(DIVIDER)
    print("  🌍 AI Travel Budget Planner")
    print(f"  Destination : {destination.title()}")
    print(f"  Budget      : ${budget_usd} USD")
    print(f"  Duration    : {num_days} days")
    print(DIVIDER)


def print_plan(plan: str) -> None:
    """Print the finalised travel plan with header and footer dividers.

    Args:
        plan (str): The formatted travel plan string produced by the
                    Orchestrator Agent.

    Example output:
        ============================================================
          📋 YOUR PERSONALISED TRAVEL PLAN
        ============================================================
        <plan content>
        ============================================================
    """
    print("\n" + DIVIDER)
    print("  📋 YOUR PERSONALISED TRAVEL PLAN")
    print(DIVIDER)
    print(plan)
    print(DIVIDER)
