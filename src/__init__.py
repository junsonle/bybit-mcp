"""Shared FastMCP server instance."""

from fastmcp import FastMCP

mcp = FastMCP("Bybit MCP Server")

__all__ = ["mcp"]
