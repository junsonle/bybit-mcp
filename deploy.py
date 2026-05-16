"""
Bybit MCP Server - Deploy to Prefect Horizon: https://horizon.prefect.io/

Entrypoint: deploy.py
Exports: mcp (FastMCP server instance)
"""

import os
from mcp.server.fastmcp import FastMCP

# 1. Tạo MCP server trực tiếp tại đây - fastmcp inspect sẽ tìm biến này
mcp = FastMCP("Bybit MCP Server")

# 2. Patch src.mcp trỏ về instance này để tools đăng ký đúng chỗ
import src
src.mcp = mcp

# 3. Import tools để đăng ký với mcp ở trên
import src.tools  # noqa: F401


def _setup():
    """Configure Bybit client at runtime."""
    from dotenv import load_dotenv
    load_dotenv()

    api_key = os.environ.get("BYBIT_API_KEY", "")
    secret_key = os.environ.get("BYBIT_SECRET_KEY", "")
    testnet = os.environ.get("BYBIT_TESTNET", "false").lower() in ("true", "1", "yes")

    from src.client import config
    config.configure(api_key=api_key, secret_key=secret_key, testnet=testnet)


from prefect import flow


@flow(name="bybit-mcp-server", log_prints=True)
def mcp_server_flow(
    transport: str = "sse",
    host: str = "0.0.0.0",
    port: int = 8000,
):
    """Run the Bybit MCP Server."""
    _setup()

    from src.client import config
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
