"""
Bybit MCP Server - Deploy to Prefect Horizon: https://horizon.prefect.io/

Entrypoint: deploy.py (exports: mcp)
"""

import os
import logging
from dotenv import load_dotenv
from prefect import flow

# Load env vars
load_dotenv()

# Configure Bybit client
api_key = os.environ.get("BYBIT_API_KEY", "")
secret_key = os.environ.get("BYBIT_SECRET_KEY", "")
testnet = os.environ.get("BYBIT_TESTNET", "false").lower() in ("true", "1", "yes")

from src.client import config
config.configure(api_key=api_key, secret_key=secret_key, testnet=testnet)

# Register tools
import src.tools  # noqa: F401

# Export MCP server (fastmcp inspect looks for: mcp, server, or app)
from src import mcp  # noqa: E402

logger = logging.getLogger("bybit-prefect")


@flow(name="bybit-mcp-server", log_prints=True)
def mcp_server_flow(
    transport: str = "sse",
    host: str = "0.0.0.0",
    port: int = 8000,
):
    """Run the Bybit MCP Server."""
    print(f"Bybit MCP Server starting")
    print(f"  base_url: {config.base_url}")
    print(f"  has_credentials: {config.has_credentials}")
    print(f"  transport: {transport}")

    if transport == "sse":
        mcp.run(transport="sse", host=host, port=port)
    else:
        mcp.run(transport="stdio")


if __name__ == "__main__":
    mcp_server_flow()
