"""
Bybit MCP Server - Deploy to Prefect Horizon: https://horizon.prefect.io/

Entrypoint: run.py (not deploy.py - avoids fastmcp run asyncio conflict)
"""

# MUST be first: patch asyncio.run to handle nested loops
import asyncio
import nest_asyncio
nest_asyncio.apply()

# Patch asyncio.run to reuse existing loop
_original_asyncio_run = asyncio.run
def _safe_run(coro, **kwargs):
    try:
        loop = asyncio.get_running_loop()
        # Already in a loop - schedule and wait
        import concurrent.futures
        future = asyncio.run_coroutine_threadsafe(coro, loop)
        return future.result()
    except RuntimeError:
        return _original_asyncio_run(coro, **kwargs)
asyncio.run = _safe_run

import os
from mcp.server.fastmcp import FastMCP

# Create MCP server
mcp = FastMCP("Bybit MCP Server")

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

# Run the server
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8081))
    mcp.run(transport="sse", host="0.0.0.0", port=port)
