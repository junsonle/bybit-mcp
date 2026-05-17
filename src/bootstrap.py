"""Shared startup helpers for local and Horizon execution."""

from __future__ import annotations

import logging
import os

from dotenv import load_dotenv

from src.client import config

LOG_FORMAT = "%(asctime)s [%(levelname)s] %(name)s: %(message)s"


def configure_bybit(
    *,
    log_level: str | None = None,
    api_key: str | None = None,
    secret_key: str | None = None,
    testnet: bool | None = None,
) -> None:
    load_dotenv()

    selected_log_level = (log_level or os.environ.get("BYBIT_LOG_LEVEL", "INFO")).upper()
    logging.basicConfig(
        level=getattr(logging, selected_log_level, logging.INFO),
        format=LOG_FORMAT,
    )

    env_testnet = os.environ.get("BYBIT_TESTNET", "").lower() in ("true", "1", "yes")
    config.configure(
        api_key=api_key if api_key is not None else os.environ.get("BYBIT_API_KEY", ""),
        secret_key=secret_key if secret_key is not None else os.environ.get("BYBIT_SECRET_KEY", ""),
        testnet=env_testnet if testnet is None else testnet,
    )


def register_tools() -> None:
    import src.tools  # noqa: F401
