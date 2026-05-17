from typing import Any

from src import mcp
from src.client import _public_get


@mcp.tool()
def get_symbol_price(symbol: str, category: str = "spot") -> Any:
    """
    Get the current price of a cryptocurrency pair.

    Args:
        symbol: The trading pair, e.g., BTCUSDT.
        category: Product type: spot, linear, inverse (default: spot).

    Returns:
        Price information from Bybit.
    """
    result = _public_get("/v5/market/tickers", {"category": category, "symbol": symbol})
    if "error" in result:
        return result
    tickers = result.get("list", [])
    if tickers:
        return {"symbol": symbol, "price": tickers[0]["lastPrice"]}
    return {"error": "No ticker data found"}


@mcp.tool()
def get_funding_rate_history(symbol: str, category: str = "linear", limit: int = 100) -> Any:
    """
    Get funding rate history for a perpetual contract.

    Args:
        symbol: Perpetual contract symbol, e.g., BTCUSDT.
        category: Product type: linear, inverse (default: linear).
        limit: Number of records to return (default: 100, max: 200).

    Returns:
        Funding rate data list.
    """
    result = _public_get("/v5/market/funding/history", {
        "category": category, "symbol": symbol, "limit": str(limit),
    })
    if "error" in result:
        return result
    return result.get("list", [])


@mcp.tool()
def get_kline(symbol: str, interval: str = "60", category: str = "spot", limit: int = 100) -> Any:
    """
    Get kline/candlestick data.

    Args:
        symbol: The trading pair, e.g., BTCUSDT.
        interval: Kline interval: 1,3,5,15,30,60,120,240,360,720,D,M,W (default: 60).
        category: Product type: spot, linear, inverse (default: spot).
        limit: Number of records (default: 100, max: 1000).

    Returns:
        List of kline data [startTime, openPrice, highPrice, lowPrice, closePrice, volume, turnover].
    """
    result = _public_get("/v5/market/kline", {
        "category": category, "symbol": symbol, "interval": interval, "limit": str(limit),
    })
    if "error" in result:
        return result
    return result.get("list", [])


@mcp.tool()
def get_orderbook(symbol: str, category: str = "spot", limit: int = 25) -> Any:
    """
    Get order book depth data.

    Args:
        symbol: The trading pair, e.g., BTCUSDT.
        category: Product type: spot, linear, inverse (default: spot).
        limit: Depth limit: 1-200 (default: 25).

    Returns:
        Order book with bids and asks.
    """
    return _public_get("/v5/market/orderbook", {
        "category": category, "symbol": symbol, "limit": str(limit),
    })


@mcp.tool()
def get_instruments_info(symbol: str, category: str = "spot") -> Any:
    """
    Get instrument specification info.

    Args:
        symbol: The trading pair, e.g., BTCUSDT.
        category: Product type: spot, linear, inverse, option (default: spot).

    Returns:
        Instrument specification details including lot size, price filter, etc.
    """
    result = _public_get("/v5/market/instruments-info", {
        "category": category, "symbol": symbol,
    })
    if "error" in result:
        return result
    instruments = result.get("list", [])
    if instruments:
        return instruments[0]
    return {"error": "No instrument data found"}


@mcp.tool()
def get_server_time() -> Any:
    """
    Get Bybit server time.

    Returns:
        Server time information.
    """
    return _public_get("/v5/market/time", {})


@mcp.tool()
def get_risk_limit(symbol: str, category: str = "linear") -> Any:
    """
    Get risk limit info for a symbol.

    Args:
        symbol: The trading pair, e.g., BTCUSDT.
        category: Product type: linear, inverse (default: linear).

    Returns:
        Risk limit tiers for the symbol.
    """
    result = _public_get("/v5/market/risk-limit", {
        "category": category, "symbol": symbol,
    })
    if "error" in result:
        return result
    return result.get("list", [])


@mcp.tool()
def get_tickers(category: str = "spot") -> Any:
    """
    Get tickers for all symbols in a category.

    Args:
        category: Product type: spot, linear, inverse, option (default: spot).

    Returns:
        List of all tickers for the category.
    """
    result = _public_get("/v5/market/tickers", {"category": category})
    if "error" in result:
        return result
    return result.get("list", [])


@mcp.tool()
def get_adl_alert(symbol: str = "") -> Any:
    """
    Get ADL (Auto-Deleveraging) alert info.

    Args:
        symbol: Contract name, e.g., BTCUSDT (optional).
    """
    params: dict[str, str] = {}
    if symbol:
        params["symbol"] = symbol
    return _public_get("/v5/market/adlAlert", params)


@mcp.tool()
def get_delivery_price(category: str, symbol: str = "", limit: int = 50) -> Any:
    """
    Get delivery price for futures/options.

    Args:
        category: Product type: linear, inverse, option.
        symbol: Symbol name (optional).
        limit: Number of records (default: 50, max: 200).
    """
    params: dict[str, str] = {"category": category, "limit": str(limit)}
    if symbol:
        params["symbol"] = symbol
    return _public_get("/v5/market/delivery-price", params)


@mcp.tool()
def get_fee_group_info(product_type: str = "contract", group_id: str = "") -> Any:
    """
    Get fee group structure info.

    Args:
        product_type: Product type: contract.
        group_id: Group ID: 1-7 (optional).
    """
    params: dict[str, str] = {"productType": product_type}
    if group_id:
        params["groupId"] = group_id
    return _public_get("/v5/market/fee-group-info", params)


@mcp.tool()
def get_index_price_components(index_name: str) -> Any:
    """
    Get index price components.

    Args:
        index_name: Index name, e.g., BTCUSDT.
    """
    return _public_get("/v5/market/index-price-components", {"indexName": index_name})


@mcp.tool()
def get_index_price_kline(symbol: str, interval: str, category: str = "linear", limit: int = 200) -> Any:
    """
    Get index price kline data.

    Args:
        symbol: Symbol, e.g., BTCUSDT.
        interval: Kline interval: 1,3,5,15,30,60,120,240,360,720,D,W,M.
        category: Product type: linear, inverse (default: linear).
        limit: Number of records (default: 200, max: 1000).
    """
    return _public_get("/v5/market/index-price-kline", {
        "symbol": symbol, "interval": interval, "category": category, "limit": str(limit),
    })


@mcp.tool()
def get_insurance(coin: str = "") -> Any:
    """
    Get insurance pool data.

    Args:
        coin: Coin name (optional, returns all if empty).
    """
    params: dict[str, str] = {}
    if coin:
        params["coin"] = coin
    return _public_get("/v5/market/insurance", params)


@mcp.tool()
def get_historical_volatility(category: str = "option", base_coin: str = "BTC", period: int = 7) -> Any:
    """
    Get historical volatility for options.

    Args:
        category: Product type: option.
        base_coin: Base coin (default: BTC).
        period: Period in days (default: 7).
    """
    return _public_get("/v5/market/historical-volatility", {
        "category": category, "baseCoin": base_coin, "period": str(period),
    })


@mcp.tool()
def get_long_short_ratio(category: str, symbol: str, period: str, limit: int = 50) -> Any:
    """
    Get long/short ratio (account ratio).

    Args:
        category: Product type: linear, inverse.
        symbol: Symbol, e.g., BTCUSDT.
        period: Period: 5min, 15min, 30min, 1h, 4h, 1d.
        limit: Number of records (default: 50, max: 500).
    """
    return _public_get("/v5/market/account-ratio", {
        "category": category, "symbol": symbol, "period": period, "limit": str(limit),
    })


@mcp.tool()
def get_mark_price_kline(symbol: str, interval: str, category: str = "linear", limit: int = 200) -> Any:
    """
    Get mark price kline data.

    Args:
        symbol: Symbol, e.g., BTCUSDT.
        interval: Kline interval: 1,3,5,15,30,60,120,240,360,720,D,M,W.
        category: Product type: linear, inverse (default: linear).
        limit: Number of records (default: 200, max: 1000).
    """
    return _public_get("/v5/market/mark-price-kline", {
        "symbol": symbol, "interval": interval, "category": category, "limit": str(limit),
    })


@mcp.tool()
def get_new_delivery_price(category: str = "option", base_coin: str = "BTC") -> Any:
    """
    Get new delivery price for options.

    Args:
        category: Product type: option.
        base_coin: Base coin (default: BTC).
    """
    return _public_get("/v5/market/new-delivery-price", {
        "category": category, "baseCoin": base_coin,
    })


@mcp.tool()
def get_open_interest(category: str, symbol: str, interval_time: str, limit: int = 50) -> Any:
    """
    Get open interest data.

    Args:
        category: Product type: linear, inverse.
        symbol: Symbol, e.g., BTCUSDT.
        interval_time: Interval: 5min, 15min, 30min, 1h, 4h, 1d.
        limit: Number of records (default: 50, max: 200).
    """
    return _public_get("/v5/market/open-interest", {
        "category": category, "symbol": symbol, "intervalTime": interval_time, "limit": str(limit),
    })


@mcp.tool()
def get_price_limit(symbol: str, category: str = "linear") -> Any:
    """
    Get order price limit for a symbol.

    Args:
        symbol: Symbol, e.g., BTCUSDT.
        category: Product type: spot, linear, inverse (default: linear).
    """
    return _public_get("/v5/market/price-limit", {"symbol": symbol, "category": category})


@mcp.tool()
def get_premium_index_price_kline(symbol: str, interval: str, category: str = "linear", limit: int = 200) -> Any:
    """
    Get premium index price kline data.

    Args:
        symbol: Symbol, e.g., BTCUSDT.
        interval: Kline interval: 1,3,5,15,30,60,120,240,360,720,D,W,M.
        category: Product type: linear (default: linear).
        limit: Number of records (default: 200, max: 1000).
    """
    return _public_get("/v5/market/premium-index-price-kline", {
        "symbol": symbol, "interval": interval, "category": category, "limit": str(limit),
    })


@mcp.tool()
def get_recent_trade(category: str, symbol: str = "", limit: int = 60) -> Any:
    """
    Get recent public trades.

    Args:
        category: Product type: spot, linear, inverse, option.
        symbol: Symbol (required for spot/linear/inverse).
        limit: Number of records (default: 60 for spot, 500 for others).
    """
    params: dict[str, str] = {"category": category, "limit": str(limit)}
    if symbol:
        params["symbol"] = symbol
    return _public_get("/v5/market/recent-trade", params)


@mcp.tool()
def get_rpi_orderbook(symbol: str, limit: int, category: str = "spot") -> Any:
    """
    Get RPI (Retail Price Improvement) orderbook.

    Args:
        symbol: Symbol, e.g., BTCUSDT.
        limit: Depth limit: 1-50.
        category: Product type: spot, linear, inverse (optional).
    """
    return _public_get("/v5/market/rpi_orderbook", {
        "symbol": symbol, "limit": str(limit), "category": category,
    })
