"""
Prefect deployment for Bybit MCP Server.

Deploy to Prefect Horizon: https://horizon.prefect.io/

Entrypoint: deploy.py:mcp_server_flow
"""

import os
import logging
from prefect import flow

logger = logging.getLogger("bybit-prefect")


@flow(name="bybit-mcp-server", log_prints=True)
def mcp_server_flow(
    transport: str = "sse",
    host: str = "0.0.0.0",
    port: int = 8000,
):
    """
    Run the Bybit MCP Server.

    Args:
        transport: "sse" (for Horizon) or "stdio" (local)
        host: Host for SSE transport
        port: Port for SSE transport
    """
    from dotenv import load_dotenv
    load_dotenv()

    api_key = os.environ.get("BYBIT_API_KEY", "")
    secret_key = os.environ.get("BYBIT_SECRET_KEY", "")
    testnet = os.environ.get("BYBIT_TESTNET", "false").lower() in ("true", "1", "yes")

    from src.client import config
    config.configure(api_key=api_key, secret_key=secret_key, testnet=testnet)

    print(f"Bybit MCP Server starting")
    print(f"  base_url: {config.base_url}")
    print(f"  has_credentials: {config.has_credentials}")
    print(f"  transport: {transport}")
    print(f"  host: {host}")
    print(f"  port: {port}")

    import src.tools  # noqa: F401
    from src import mcp

    if transport == "sse":
        mcp.run(transport="sse", host=host, port=port)
    else:
        mcp.run(transport="stdio")


if __name__ == "__main__":
    mcp_server_flow()
