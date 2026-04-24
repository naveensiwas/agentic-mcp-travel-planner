"""
Central configuration module for the AI Travel Budget Planner.

Responsibilities:
  - LLM factory: creates a shared ChatGroq instance used by all agents.
  - Server config builder: returns MCP server connection dicts with
    correct absolute paths so agents can be run from any working directory.
  - Application constants: CURRENCY_MAP for destination → local currency lookup.

Environment Variables (loaded via .env):
  GROQ_API_KEY  (required) — Groq cloud API key
  GROQ_MODEL    (optional) — model name, default: qwen/qwen3-32b
"""

import os
from pathlib import Path
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.utils import convert_to_secret_str

# Load .env from the project root (one level above this config/ folder)
load_dotenv(dotenv_path=Path(__file__).parent.parent / ".env")

# Absolute path to the servers/ directory — used to build subprocess args
# so agents work correctly regardless of the current working directory.
SERVERS_DIR = Path(__file__).parent.parent / "servers"


# ─────────────────────────────────────────────
# LLM Factory
# ─────────────────────────────────────────────
def get_llm() -> ChatGroq:
    """Create and return a configured ChatGroq LLM instance.

    Reads GROQ_API_KEY and GROQ_MODEL from environment / .env.
    All three agents share this factory to ensure consistent model settings.

    Returns:
        ChatGroq: Configured LLM ready for use in LangGraph agents.

    Raises:
        ValueError: If GROQ_API_KEY is not set.
    """
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        raise ValueError("GROQ_API_KEY not set. Add it to your .env file.")

    model_name = os.getenv("GROQ_MODEL", "qwen/qwen3-32b")
    return ChatGroq(model=model_name, api_key=convert_to_secret_str(api_key))


# ─────────────────────────────────────────────
# MCP Server Configuration Builder
# ─────────────────────────────────────────────
def get_server_configs() -> dict:
    """Return MCP server connection configs with absolute paths to server scripts.

    Using absolute paths (derived from this file's location) ensures the stdio
    subprocess commands work correctly no matter where main.py is invoked from.

    Returns:
        dict: Mapping of server name → MCP transport configuration.
              Keys: "weather", "travel_tips", "currency", "math"
    """
    return {
        # HTTP server — must be started manually before running main.py
        "weather": {
            "url": "http://localhost:8000/mcp",
            "transport": "streamable_http",
        },
        # stdio servers — auto-spawned as subprocesses by MultiServerMCPClient
        "travel_tips": {
            "command": "python",
            "args": [str(SERVERS_DIR / "travel_tips_server.py")],
            "transport": "stdio",
        },
        "currency": {
            "command": "python",
            "args": [str(SERVERS_DIR / "currency_server.py")],
            "transport": "stdio",
        },
        "math": {
            "command": "python",
            "args": [str(SERVERS_DIR / "math_server.py")],
            "transport": "stdio",
        },
    }


# ─────────────────────────────────────────────
# Application Constants
# ─────────────────────────────────────────────

# Maps lowercase destination name → ISO 4217 local currency code.
# Used by the Finance Agent to select the correct target currency.
# Falls back to "EUR" for any destination not listed here.
CURRENCY_MAP: dict[str, str] = {
    "tokyo":    "JPY",
    "paris":    "EUR",
    "new york": "USD",
    "bali":     "IDR",
}
