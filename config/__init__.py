"""
Config Package
==============
Centralised configuration for the AI Travel Budget Planner.

Modules:
  - settings : LLM factory, server path helpers, and application constants.
"""
from config.settings import get_llm, get_server_configs, CURRENCY_MAP

__all__ = ["get_llm", "get_server_configs", "CURRENCY_MAP"]
