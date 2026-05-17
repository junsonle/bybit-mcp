import logging
import time
import hmac
import hashlib
import json
import os
import requests

logger = logging.getLogger("bybit-mcp")


class Config:
    api_key: str = ""
    secret_key: str = ""
    base_url: str = "https://api.bybit.com"
    recv_window: str = "5000"

    def configure(self, api_key: str, secret_key: str, testnet: bool = False):
        self.api_key = api_key or ""
        self.secret_key = secret_key or ""
        custom_base_url = os.environ.get("BYBIT_BASE_URL", "").strip()
        if custom_base_url:
            self.base_url = custom_base_url.rstrip("/")
        else:
            self.base_url = "https://api-testnet.bybit.com" if testnet else "https://api.bybit.com"

    @property
    def has_credentials(self) -> bool:
        return bool(self.api_key and self.secret_key)


config = Config()

REQUEST_TIMEOUT = 20
DEFAULT_HEADERS = {
    "Accept": "application/json",
    "User-Agent": "bybit-mcp-server/0.2.0",
}


def _response_body_preview(response: requests.Response, limit: int = 500) -> str:
    return response.text.strip().replace("\r", "\\r").replace("\n", "\\n")[:limit]


def _decode_bybit_response(response: requests.Response, request_name: str) -> dict:
    try:
        data = response.json()
    except ValueError as e:
        body_preview = _response_body_preview(response)
        logger.error(
            "%s returned non-JSON response status=%s content_type=%s body=%r",
            request_name,
            response.status_code,
            response.headers.get("content-type", ""),
            body_preview,
        )
        return {
            "error": "Bybit returned a non-JSON response",
            "parse_error": str(e),
            "status_code": response.status_code,
            "content_type": response.headers.get("content-type", ""),
            "url": response.url,
            "body_preview": body_preview,
        }

    if not isinstance(data, dict):
        return {
            "error": "Bybit returned an unexpected JSON response",
            "status_code": response.status_code,
            "url": response.url,
            "body_preview": _response_body_preview(response),
        }

    return data


def _bybit_result(data: dict, request_name: str) -> dict:
    if "error" in data:
        return data
    if data.get("retCode") == 0:
        logger.debug("%s success", request_name)
        return data.get("result", {})
    logger.warning(
        "%s retCode=%s retMsg=%s",
        request_name,
        data.get("retCode"),
        data.get("retMsg"),
    )
    return {"error": data.get("retMsg", "Unknown error"), "retCode": data.get("retCode")}


def _sign_request(timestamp: str, params: str) -> str:
    """Generate HMAC-SHA256 signature for Bybit V5 API."""
    param_str = f"{timestamp}{config.api_key}{config.recv_window}{params}"
    return hmac.new(
        config.secret_key.encode("utf-8"),
        param_str.encode("utf-8"),
        hashlib.sha256,
    ).hexdigest()


def _auth_headers(timestamp: str, signature: str) -> dict:
    """Build authenticated request headers."""
    return {
        "X-BAPI-API-KEY": config.api_key,
        "X-BAPI-SIGN": signature,
        "X-BAPI-SIGN-TYPE": "2",
        "X-BAPI-TIMESTAMP": timestamp,
        "X-BAPI-RECV-WINDOW": config.recv_window,
        "Content-Type": "application/json",
    }


def _require_credentials():
    """Raise a clear error if API credentials are not configured."""
    if not config.has_credentials:
        return {
            "error": "API credentials not configured. "
            "Set BYBIT_API_KEY and BYBIT_SECRET_KEY via .env file or command-line arguments."
        }
    return None


def _public_get(endpoint: str, params: dict) -> dict:
    """Make an unauthenticated GET request to Bybit V5 API."""
    logger.debug("PUBLIC GET %s params=%s", endpoint, params)
    try:
        response = requests.get(
            f"{config.base_url}{endpoint}",
            headers=DEFAULT_HEADERS,
            params=params,
            timeout=REQUEST_TIMEOUT,
        )
    except requests.RequestException as e:
        logger.error("PUBLIC GET %s failed: %s", endpoint, e)
        return {"error": f"Request failed: {e}"}
    return _bybit_result(_decode_bybit_response(response, f"PUBLIC GET {endpoint}"), f"PUBLIC GET {endpoint}")


def _signed_get(endpoint: str, params: dict) -> dict:
    """Make a signed GET request to Bybit V5 API."""
    cred_error = _require_credentials()
    if cred_error:
        return cred_error
    logger.debug("SIGNED GET %s params=%s", endpoint, params)
    timestamp = str(int(time.time() * 1000))
    query_string = "&".join([f"{k}={v}" for k, v in params.items()])
    signature = _sign_request(timestamp, query_string)
    headers = {**DEFAULT_HEADERS, **_auth_headers(timestamp, signature)}
    try:
        response = requests.get(
            f"{config.base_url}{endpoint}",
            headers=headers,
            params=params,
            timeout=REQUEST_TIMEOUT,
        )
    except requests.RequestException as e:
        logger.error("SIGNED GET %s failed: %s", endpoint, e)
        return {"error": f"Request failed: {e}"}
    return _bybit_result(_decode_bybit_response(response, f"SIGNED GET {endpoint}"), f"SIGNED GET {endpoint}")


def _signed_post(endpoint: str, params: dict) -> dict:
    """Make a signed POST request to Bybit V5 API."""
    cred_error = _require_credentials()
    if cred_error:
        return cred_error
    logger.debug("SIGNED POST %s params=%s", endpoint, params)
    timestamp = str(int(time.time() * 1000))
    body = json.dumps(params)
    signature = _sign_request(timestamp, body)
    headers = {**DEFAULT_HEADERS, **_auth_headers(timestamp, signature)}
    try:
        response = requests.post(
            f"{config.base_url}{endpoint}",
            headers=headers,
            data=body,
            timeout=REQUEST_TIMEOUT,
        )
    except requests.RequestException as e:
        logger.error("SIGNED POST %s failed: %s", endpoint, e)
        return {"error": f"Request failed: {e}"}
    return _bybit_result(_decode_bybit_response(response, f"SIGNED POST {endpoint}"), f"SIGNED POST {endpoint}")
