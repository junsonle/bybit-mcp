"""
Bybit MCP Server - Deploy to Prefect Horizon: https://horizon.prefect.io/

Entrypoint: deploy.py
Exports: mcp (FastMCP server instance)
"""

# Allow nested event loops (Horizon already has one running)
import nest_asyncio
nest_asyncio.apply()

import os
from mcp.server.fastmcp import FastMCP

# 1. Create MCP server - fastmcp inspect looks for: mcp, server, or app
mcp = FastMCP("Bybit MCP Server")

# 2. Patch src.mcp so tools register with THIS instance
import src
src.mcp = mcp

# 3. Register all tools
import src.tools  # noqa: F401

# 4. Configure Bybit client
from dotenv import load_dotenv
load_dotenv()

api_key = os.environ.get("BYBIT_API_KEY", "")
secret_key = os.environ.get("BYBIT_SECRET_KEY", "")
testnet = os.environ.get("BYBIT_TESTNET", "false").lower() in ("true", "1", "yes")

from src.client import config
config.configure(api_key=api_key, secret_key=secret_key, testnet=testnet)
