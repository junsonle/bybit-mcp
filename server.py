"""Prefect Horizon entrypoint for the Bybit MCP server.

Horizon imports this file and looks for a FastMCP instance named ``mcp``.
"""

from src import mcp
from src.bootstrap import configure_bybit, register_tools

configure_bybit()
register_tools()


if __name__ == "__main__":
    mcp.run()
