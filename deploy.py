"""
Bybit MCP Server - Deploy to Prefect Horizon: https://horizon.prefect.io/

Entrypoint: deploy.py
Exports: mcp (FastMCP server instance)
"""

import os
import asyncio
from mcp.server.fastmcp import FastMCP


class HorizonFastMCP(FastMCP):
    """FastMCP subclass that handles nested event loops (required for Horizon)."""

    def run(self, transport=None, host=None, port=None):
        """Override run to use existing event loop if available."""
        import nest_asyncio
        try:
            nest_asyncio.apply()
        except Exception:
            pass

        try:
            loop = asyncio.get_running_loop()
            # Already in a loop - run coroutine directly
            return loop.run_until_complete(
                self.run_async(transport=transport, host=host, port=port)
            )
        except RuntimeError:
            # No loop yet - use normal asyncio.run
            return super().run(transport=transport, host=host, port=port)


# Create MCP server - fastmcp inspect looks for: mcp, server, or app
mcp = HorizonFastMCP("Bybit MCP Server")

# Patch src.mcp so tools register with THIS instance
import src
src.mcp = mcp

# Register all tools
import src.tools  # noqa: F401

# Configure Bybit client
from dotenv import load_dotenv
load_dotenv()

api_key = os.environ.get("BYBIT_API_KEY", "")
secret_key = os.environ.get("BYBIT_SECRET_KEY", "")
testnet = os.environ.get("BYBIT_TESTNET", "false").lower() in ("true", "1", "yes")

from src.client import config
config.configure(api_key=api_key, secret_key=secret_key, testnet=testnet)
