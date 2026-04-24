"""
MCP Math Server
===============
A lightweight MCP (Model Context Protocol) server that exposes basic
mathematical operations as callable tools for AI agents.

Tools provided:
  • add(a, b)      → Returns the sum of two integers
  • multiply(a, b) → Returns the product of two integers

Transport: stdio
  - The server communicates via standard input/output (stdin/stdout).
  - This makes it easy to spawn as a subprocess from MCP clients
    (e.g. MultiServerMCPClient in project entry scripts).

Usage:
  Run directly:
    python servers/math_server.py

  Or let an MCP client spawn it automatically via stdio transport config:
    {
        "math": {
            "command": "python",
            "args": ["servers/math_server.py"],
            "transport": "stdio"
        }
    }
"""

from mcp.server.fastmcp import FastMCP

# Initialise the FastMCP server with the name "Math".
# This name is used by MCP clients to identify the server.
mcp = FastMCP("Math")


@mcp.tool()
def add(a: int, b: int) -> int:
    """Add two integers and return the result.

    Args:
        a (int): The first number.
        b (int): The second number.

    Returns:
        int: The sum of a and b.
    """
    return a + b


@mcp.tool()
def multiply(a: int, b: int) -> int:
    """Multiply two integers and return the result.

    Args:
        a (int): The first number.
        b (int): The second number.

    Returns:
        int: The product of a and b.
    """
    return a * b


if __name__ == "__main__":
    # Start the MCP server using stdio transport.
    # The server will listen on stdin for incoming tool-call requests
    # and write responses back to stdout.
    # This mode is ideal for subprocess-based MCP client integration.
    mcp.run(transport="stdio")
