"""
Bybit MCP Server - Deploy to Prefect Horizon: https://horizon.prefect.io/

Entrypoint: deploy.py
Exports: mcp (FastMCP server instance)
"""

import os
import asyncio
import threading
from mcp.server.fastmcp import FastMCP


class HorizonMCP(FastMCP):
    """FastMCP subclass that reuses existing event loop (required for Horizon)."""

    def run(self, transport=None, mount_path=None):
        try:
            loop = asyncio.get_running_loop()
            # We're already in a running loop (Horizon context).
            # Schedule the task and block main thread until it completes.
            done = threading.Event()

            async def _run_and_signal():
                try:
                    if transport == "sse":
                        await self.run_sse_async(mount_path=mount_path)
                    elif transport == "streamable-http":
                        await self.run_streamable_http_async()
                    else:
                        await self.run_stdio_async()
                finally:
                    done.set()

            loop.create_task(_run_and_signal())
            # Block the main thread while async server runs in background
            done.wait()
        except RuntimeError:
            # No loop yet - use normal FastMCP.run
            return super().run(transport=transport, mount_path=mount_path)


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
