"""
Bybit MCP Server - Deploy to Prefect Horizon: https://horizon.prefect.io/

Entrypoint: deploy.py
Exports: mcp (FastMCP server instance)
"""

import os
import asyncio
from mcp.server.fastmcp import FastMCP


class HorizonMCP(FastMCP):
    """FastMCP subclass that reuses existing event loop (required for Horizon)."""

    def run(self, transport=None, host=None, port=None):
        try:
            loop = asyncio.get_running_loop()
            # We're already in a running loop (Horizon context).
            # Schedule run_async as a task and return immediately.
            asyncio.create_task(self.run_async(transport=transport, host=host, port=port))
        except RuntimeError:
            # No loop yet - use normal asyncio.run
            return super().run(transport=transport, host=host, port=port)


# Create MCP server - fastmcp inspect looks for: mcp, server, or app
mcp = HorizonMCP("Bybit MCP Server")

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
