<div align="center">

# 🟡 Bybit MCP Server

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.13+](https://img.shields.io/badge/python-3.13+-blue.svg)](https://www.python.org/downloads/)
[![MCP](https://img.shields.io/badge/MCP-compatible-purple.svg)](https://modelcontextprotocol.io)
[![Tools](https://img.shields.io/badge/Tools-246-orange.svg)](#-available-tools-246)
[![Bybit V5 API](https://img.shields.io/badge/Bybit-V5%20API-green.svg)](https://bybit-exchange.github.io/docs/v5/intro)

**The most comprehensive MCP server for Bybit — 247 tools covering the entire Bybit V5 API**

[Quick Start](#-quick-start) •
[Features](#-features) •
[Configuration](#%EF%B8%8F-configuration) •
[Tools Reference](#-available-tools-246) •
[Troubleshooting](#-troubleshooting) •
[Contributing](#-contributing)

</div>

---

## 🎯 Overview

Bybit MCP Server enables AI assistants like **Claude**, **Cursor**, **ChatGPT**, and other MCP-compatible clients to interact directly with the Bybit cryptocurrency exchange. Execute trades, manage portfolios, analyze markets, and automate strategies — all through natural language.

### Why Bybit MCP?

- **🔥 Complete Coverage** — 247 tools spanning every Bybit V5 API endpoint
- **🔐 Secure by Design** — API credentials never leave your machine
- **👁️ Read-Only Mode** — Use all market tools without any API key
- **📡 Remote-ready Transport** — STDIO for local clients, HTTP/SSE for remote testing
- **🔌 Universal Compatibility** — Works with Claude Desktop, Cursor, ChatGPT, and any MCP client
- **⚡ Zero Config Start** — Just `uv run bybit.py` and go

---

## ✨ Features

<table>
<tr>
<td width="50%">

### 📈 Trading & Markets
- **Spot Trading** — Market & limit orders, batch operations
- **Derivatives** — Linear & inverse perpetuals
- **Order Management** — Amend, cancel, batch, DCP
- **Market Data** — Klines, orderbook, tickers, funding rates
- **Open Interest** — Long/short ratio, ADL alerts

</td>
<td width="50%">

### 💰 Earn & Lending
- **Simple Earn** — Stake, redeem, yield tracking
- **Crypto Loans** — Old & new (fixed + flexible)
- **Leveraged Tokens** — Subscribe & redeem
- **Spot Margin** — Cross-margin trading
- **OTC Lending** — Institutional loan management

</td>
</tr>
<tr>
<td width="50%">

### 🏦 Account & Assets
- **Wallet** — Deposits, withdrawals, transfers
- **Multi-Account** — Sub-accounts, universal transfers
- **Asset Convert** — Crypto-to-crypto, small balance, fiat
- **Margin Modes** — Cross, isolated, portfolio margin
- **Risk Management** — MMP, leverage, TP/SL

</td>
<td width="50%">

### 🛠️ Advanced
- **Spread Trading** — Spread instruments & orders
- **Block Trading (RFQ)** — Request for quote workflow
- **Broker** — Earnings, rate limits, vouchers
- **Strategy** — Built-in arbitrage detection
- **Announcements** — Exchange news & system status

</td>
</tr>
</table>

---

## 🚀 Quick Start

### Method 1: Ask AI to Install (Recommended)

Simply tell your AI assistant:

> **"Help me install the Bybit MCP server from https://github.com/JohnnyWic/bybit-mcp"**

Your AI will clone the repo, install dependencies, and configure everything automatically. Works with Claude Code, Cursor, and other MCP-compatible clients.

### Method 2: Manual Setup

#### 1. Install

```bash
git clone https://github.com/JohnnyWic/bybit-mcp.git
cd bybit-mcp
uv sync
```

> Requires [Python ≥ 3.13](https://www.python.org/downloads/) and [uv](https://docs.astral.sh/uv/).

#### 2. Add to Your MCP Client

Add the following to your MCP config file:

| Client | Config File |
|--------|------------|
| Claude Desktop | `claude_desktop_config.json` |
| Cursor | `~/.cursor/mcp.json` |
| Claude Code | Run `claude mcp add` (see below) |

**JSON config (Claude Desktop / Cursor):**

```json
{
  "mcpServers": {
    "bybit-mcp": {
      "command": "uv",
      "args": ["--directory", "/path/to/bybit-mcp", "run", "bybit.py"]
    }
  }
}
```

**Claude Code CLI:**

```bash
claude mcp add bybit-mcp -- uv --directory /path/to/bybit-mcp run bybit.py
```

#### 3. Configure API Key (Optional)

Create a `.env` file in the project root:

```bash
cp .env.example .env
```

```env
BYBIT_API_KEY=your_api_key_here
BYBIT_SECRET_KEY=your_secret_key_here
BYBIT_TESTNET=false
```

Or pass credentials inline in the MCP config:

```json
{
  "mcpServers": {
    "bybit-mcp": {
      "command": "uv",
      "args": [
        "--directory", "/path/to/bybit-mcp", "run", "bybit.py",
        "--bybit-api-key", "YOUR_API_KEY",
        "--bybit-secret-key", "YOUR_SECRET_KEY"
      ]
    }
  }
}
```

> 💡 **No API key?** No problem! All 23 market data tools work without authentication.
>
> **🔒 Security Note:** Never commit your `.env` file. It's already in `.gitignore`.

### Transport Modes

```bash
uv run bybit.py                                        # STDIO (default)
uv run bybit.py --transport http --port 8000            # HTTP
uv run bybit.py --transport sse --port 8000             # SSE
```

### Deploy to Prefect Horizon

Horizon imports a Python file and looks for a FastMCP server object. Use this configuration at <https://horizon.prefect.io/>:

| Field | Value |
|-------|-------|
| Entrypoint | `server.py:mcp` |
| Requirements | `pyproject.toml` or leave blank |
| Environment | Set `BYBIT_API_KEY`, `BYBIT_SECRET_KEY`, and `BYBIT_TESTNET` in Horizon |

No `prefect.yaml`, `deploy.py`, Dockerfile, or custom deploy script is required. Push this repo to GitHub, select it in Horizon, enter `server.py:mcp`, and deploy.

---

## 💬 Usage Examples

### Check Market Price

```
"What's the current price of BTC?"
```

### Place a Trade

```
"Buy 0.01 BTC at market price on spot"
```

### Analyze Funding Rates

```
"Show me the funding rate history for ETHUSDT over the last 24 hours"
```

### Manage Positions

```
"What are my open positions? Set a stop loss at 95000 for my BTCUSDT long"
```

### Portfolio Overview

```
"Show my unified account balance and all open orders"
```

---

## 📊 Available Tools (246)

| Module | Tools | Description |
|--------|------:|-------------|
| **Market** | 23 | Prices, klines, orderbook, funding rates, open interest, tickers *(no API key needed)* |
| **Trade** | 15 | Market/limit orders, amend, cancel, batch operations, DCP |
| **Account** | 25 | Balance, fee rates, margin mode, collateral, MMP, transaction log |
| **Position** | 11 | Positions, leverage, TP/SL, auto-margin, move positions |
| **Asset** | 41 | Deposits, withdrawals, transfers, convert, fiat, address management |
| **Lending** | 39 | Crypto loans — legacy + new (fixed & flexible) |
| **User** | 15 | Sub-accounts, API key management, affiliate |
| **RFQ** | 15 | Block trading — create/cancel RFQ, quotes, executions |
| **Spot Margin** | 12 | Spot margin trading, borrow, repay, collateral |
| **Spread** | 11 | Spread instruments, orderbook, trading |
| **Broker** | 10 | Broker earnings, rate limits, vouchers |
| **OTC** | 7 | Institutional OTC lending |
| **Pre-Upgrade** | 6 | Pre-upgrade historical data queries |
| **Earn** | 6 | Staking, redemption, yield tracking |
| **Leveraged Token** | 5 | Leveraged token subscribe/redeem |
| **Announcement** | 2 | Exchange announcements, system status |
| **Strategy** | 2 | Built-in arbitrage pair detection |

**Total: 246 tools**

<details>
<summary><b>📋 View all tool names</b></summary>

```bash
uv run fastmcp inspect server.py:mcp
```

</details>

---

## 🏗️ Project Structure

```
bybit-mcp/
├── server.py                   # Prefect Horizon entrypoint: server.py:mcp
├── bybit.py                    # Entry point (backward compatible)
├── src/
│   ├── __init__.py             # Shared FastMCP instance
│   ├── bootstrap.py            # Env loading + Bybit client setup
│   ├── main.py                 # CLI: dotenv + argparse + logging + mcp.run()
│   ├── client.py               # Config singleton + HMAC signing + HTTP methods
│   └── tools/
│       ├── __init__.py         # Auto-imports all tool modules
│       ├── market.py           # 23 tools — public market data
│       ├── trade.py            # 15 tools — order management
│       ├── account.py          # 25 tools — account operations
│       ├── position.py         # 11 tools — position management
│       ├── asset.py            # 41 tools — wallet & transfers
│       ├── lending.py          # 39 tools — crypto loans
│       ├── earn.py             #  6 tools — staking & yield
│       ├── leveraged_token.py  #  5 tools — leveraged tokens
│       ├── spot_margin.py      # 12 tools — spot margin
│       ├── user.py             # 15 tools — sub-accounts & API keys
│       ├── broker.py           # 10 tools — broker services
│       ├── otc.py              #  7 tools — OTC lending
│       ├── spread.py           # 11 tools — spread trading
│       ├── rfq.py              # 15 tools — block trading RFQ
│       ├── pre_upgrade.py      #  6 tools — pre-upgrade data
│       ├── announcement.py     #  2 tools — announcements
│       └── strategy.py         #  2 tools — arbitrage strategies
├── .env.example                # Environment variable template
├── pyproject.toml              # Project config & dependencies
└── LICENSE                     # MIT License
```

---

## 🔧 Troubleshooting

### MCP Server Not Loading / "No MCP servers configured"

If you've configured the server but `/mcp` shows no tools or "No MCP servers configured":

#### 1. Check the correct configuration file

Claude Code reads MCP server config from `~/.claude.json` (per-project), **not** from `~/.claude/settings.json`. The recommended way to add the server is via CLI:

```bash
claude mcp add bybit-mcp -- uv --directory /path/to/bybit-mcp run bybit.py
```

This writes the config to the correct location. If you manually edited `~/.claude/settings.json`, the server won't be found.

#### 2. Use the full path to `uv`

Claude Code spawns MCP server subprocesses **without loading your shell profile** (`.zshrc` / `.zprofile`), so `PATH` may not include `~/.local/bin`. Use the absolute path:

```bash
# Find your uv path
which uv
# Example output: /Users/yourname/.local/bin/uv

# Add with full path
claude mcp add bybit-mcp -- /Users/yourname/.local/bin/uv --directory /path/to/bybit-mcp run bybit.py
```

#### 3. Restart Claude Code after configuration changes

MCP servers connect at session startup. After adding or changing config, you must **exit and restart** Claude Code for changes to take effect.

#### 4. Verify the server starts correctly

Test that the server can start and respond to MCP protocol:

```bash
# Test import
uv run python -c "from server import mcp; print('Import OK')"

# Inspect what Horizon will see
uv run fastmcp inspect server.py:mcp

# Test MCP initialize handshake
echo '{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2024-11-05","capabilities":{},"clientInfo":{"name":"test","version":"0.1"}}}' | uv run bybit.py
```

If the import fails, run `uv sync` to install dependencies.

#### 5. Don't run the server manually

Claude Code manages the MCP server process itself via stdio. A manually started server instance is **completely separate** — Claude Code won't connect to it. Let Claude Code handle the lifecycle automatically.

### Quick Diagnosis Checklist

| Symptom | Cause | Fix |
|---------|-------|-----|
| `/mcp` shows "No MCP servers configured" | Config in wrong file (`settings.json` instead of `.claude.json`) | Use `claude mcp add` CLI command |
| Config exists but tools don't load | `uv` not found (PATH issue) | Use absolute path to `uv` |
| Tools loaded before but not now | Session not restarted after config change | Restart Claude Code |
| Server works manually but not in Claude Code | Manual server is a separate process | Don't start manually; let Claude Code manage it |
| Import errors on startup | Dependencies not installed | Run `uv sync` |

---

## ⚠️ Disclaimer

This software is provided for educational and informational purposes only.

- **Not Financial Advice** — This tool does not provide financial, investment, or trading advice
- **Use at Your Own Risk** — Cryptocurrency trading involves substantial risk of loss
- **API Security** — Protect your API credentials; use IP restrictions and disable withdrawal permissions
- **Test First** — Always test on [Bybit Testnet](https://testnet.bybit.com/) before using real funds (`--testnet` flag)
- **No Warranty** — The software is provided "as is" without warranty of any kind

---

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Adding New Tools

1. Add your tool function in the appropriate `src/tools/*.py` module
2. Decorate with `@mcp.tool()`
3. Use `_public_get` for unauthenticated or `_signed_get`/`_signed_post` for authenticated endpoints
4. That's it — tools are auto-registered on import

---

## 📚 Resources

| Resource | Description |
|----------|-------------|
| [Bybit V5 API Docs](https://bybit-exchange.github.io/docs/v5/intro) | Official Bybit API documentation |
| [Bybit Testnet](https://testnet.bybit.com/) | Practice trading with test funds |
| [MCP Specification](https://modelcontextprotocol.io/) | Model Context Protocol spec |
| [FastMCP Docs](https://gofastmcp.com/) | FastMCP server framework and CLI |
| [Prefect Horizon](https://horizon.prefect.io/) | Hosted deployment for FastMCP servers |
| [uv Package Manager](https://docs.astral.sh/uv/) | Fast Python package manager |

---

## 📄 License

This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.

---

<div align="center">

**Built with ❤️ for the Bybit trading community**

</div>
