from mcp.server.fastmcp import FastMCP
import os

# mcp = FastMCP("Bybit MCP Server")

port = int(os.environ.get("PORT", 8000))
host = os.environ.get("FASTMCP_HOST", "0.0.0.0")
mcp = FastMCP("Bybit MCP Server", host=host, port=port)
