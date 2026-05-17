import argparse
import logging

from src import mcp
from src.bootstrap import configure_bybit, register_tools
from src.client import config


def main() -> None:
    parser = argparse.ArgumentParser(description="Bybit MCP Server")
    parser.add_argument(
        "--log-level",
        choices=["DEBUG", "INFO", "WARNING", "ERROR"],
        default=None,
        help="Log level (default: BYBIT_LOG_LEVEL or INFO)",
    )
    parser.add_argument(
        "--bybit-api-key",
        default=None,
        help="Bybit API key (or set BYBIT_API_KEY env var)",
    )
    parser.add_argument(
        "--bybit-secret-key",
        default=None,
        help="Bybit secret key (or set BYBIT_SECRET_KEY env var)",
    )
    parser.add_argument(
        "--testnet",
        action="store_true",
        help="Use Bybit testnet (or set BYBIT_TESTNET=true env var)",
    )
    parser.add_argument(
        "--transport",
        choices=["stdio", "http", "sse"],
        default="stdio",
        help="MCP transport type (default: stdio)",
    )
    parser.add_argument(
        "--host",
        default="127.0.0.1",
        help="Host for HTTP/SSE transport (default: 127.0.0.1)",
    )
    parser.add_argument(
        "--port",
        type=int,
        default=8000,
        help="Port for HTTP/SSE transport (default: 8000)",
    )

    args, _ = parser.parse_known_args()

    configure_bybit(
        log_level=args.log_level,
        api_key=args.bybit_api_key,
        secret_key=args.bybit_secret_key,
        testnet=True if args.testnet else None,
    )
    register_tools()

    logger = logging.getLogger("bybit-mcp")
    logger.info(
        "Bybit MCP Server starting (base_url=%s, has_credentials=%s, transport=%s)",
        config.base_url,
        config.has_credentials,
        args.transport,
    )

    if args.transport == "stdio":
        mcp.run()
    else:
        mcp.run(transport=args.transport, host=args.host, port=args.port)


if __name__ == "__main__":
    main()
