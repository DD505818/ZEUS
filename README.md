# ZEUS°NXTLVL GODMODE

ZEUS is a full-stack autonomous trading system. It includes:

- **Backend** built with FastAPI
- **Frontend** (not included here) using Next.js
- **CI/CD** scripts via GitHub Actions

This repository focuses on the core trading engine and agents. Example modules include the **ORB**, **Range**, and **Gap Sniper** strategies.

## Top Agents

The system bundles six profit-focused agents:

- **QuantumBoost** – EMA trend with RSI and volume filter
- **PredictiveProphet** – AI-based probability forecasts
- **HeikinBreakout** – Heikin-Ashi and MACD breakout logic
- **VWAPScalperX** – VWAP and RSI intraday scalper
- **RSIHeikinSniper** – RSI oversold with Heikin-Ashi reversal
- **GapSniper** – Detects breakaway gaps

## Requirements

See `requirements.txt` for Python dependencies. Install with:

```bash
pip install -r requirements.txt
```

## Running the Multi-Agent Executor

Prepare a pandas DataFrame of market data containing `open`, `high`, `low`, `close`, and `volume` columns indexed by timestamps. Then run:

```bash
python multi_agent_executor.py
```

This will execute all agents on the provided data and print broker executions.

### Nightly Capital Boost

After each trading day, `MultiAgentExecutor.nightly_update()` adjusts capital
allocations. Agents with a daily ROI over **4%** and a win rate above **85%**
receive a **7%** boost. Moderate performers with ROI above **3%** get a **3%**
increase, while underperformers below **-2%** lose **5%** of their capital.
