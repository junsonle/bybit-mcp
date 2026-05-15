import logging
import os
import argparse
import nest_asyncio
from dotenv import load_dotenv
from fastmcp import FastMCP  # ✅ Sửa import này

# ✅ Apply nest_asyncio ngay từ đầu
nest_asyncio.apply()

# ✅ Khởi tạo mcp ở đây hoặc trong main()
mcp = FastMCP("Bybit MCP Server")

def main():
    load_dotenv()
    
    parser = argparse.ArgumentParser(description="Bybit MCP Server")
    parser.add_argument("--log-level", type=str, default="INFO",
                        choices=["DEBUG", "INFO", "WARNING", "ERROR"],
                        help="Log level (default: INFO)")
    parser.add_argument("--bybit-api-key", type=str, default="",
                        help="Bybit API Key (or set BYBIT_API_KEY env var)")
    parser.add_argument("--bybit-secret-key", type=str, default="",
                        help="Bybit Secret Key (or set BYBIT_SECRET_KEY env var)")
    parser.add_argument("--testnet", action="store_true",
                        help="Use Bybit testnet (or set BYBIT_TESTNET=true env var)")
    parser.add_argument("--transport", type=str, default="stdio",
                        choices=["stdio", "sse"],  # ✅ Bỏ streamable-http nếu không dùng
                        help="MCP transport type (default: stdio)")
    parser.add_argument("--host", type=str, default="127.0.0.1",
                        help="Host for SSE transport (default: 127.0.0.1)")
    parser.add_argument("--port", type=int, default=8000,
                        help="Port for SSE transport (default: 8000)")
    
    args, _ = parser.parse_known_args()
    
    log_level = args.log_level or os.environ.get("BYBIT_LOG_LEVEL", "INFO")
    logging.basicConfig(
        level=getattr(logging, log_level.upper(), logging.INFO),
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    )
    logger = logging.getLogger("bybit-mcp")
    
    api_key = args.bybit_api_key or os.environ.get("BYBIT_API_KEY", "")
    secret_key = args.bybit_secret_key or os.environ.get("BYBIT_SECRET_KEY", "")
    testnet = args.testnet or os.environ.get("BYBIT_TESTNET", "").lower() in ("true", "1", "yes")
    
    from src.client import config
    config.configure(api_key=api_key, secret_key=secret_key, testnet=testnet)
    
    logger.info("Bybit MCP Server starting (base_url=%s, has_credentials=%s, transport=%s)",
                config.base_url, config.has_credentials, args.transport)
    
    # ✅ Import tools để register
    import src.tools  # noqa: F401
    
    # ✅ Chạy server với transport phù hợp
    if args.transport == "sse":
        mcp.run(transport="sse", host=args.host, port=args.port)
    else:
        mcp.run(transport="stdio")

if __name__ == "__main__":
    main()
