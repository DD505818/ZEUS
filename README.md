# ZEUS NXTLVL

This repository contains a simplified prototype of an autonomous trading engine. It includes a set of lightweight trading indicators and a basic orchestration engine used for demonstration purposes.  The project is intentionally minimal and does not execute real trades.

## Running the demo

Install dependencies and launch the example script:

```bash
pip install -r requirements.txt
python main.py
```

The example repeatedly generates random price data and prints the decision returned by the trading engine.

## Tests

After installing requirements you can run the unit tests:

```bash
python -m unittest discover tests
```

## Docker demo

Build and launch the containers using docker compose:

```bash
docker-compose up --build
```

This starts a demo FastAPI service on port 3000 and an Airflow UI on port 8080.

## ZEUS\u00b0NXTLVL \u2014 Top 6 Agents

Below is a high‑level reference for the primary agents used in the
`ZeusTradeEngine`. Each agent returns a buy signal only when strict
conditions are met.

| Agent | Type | Logic snippet |
|-------|------|---------------|
| **QuantumBoost** | Alpha Trend + RSI/Volume | `EMA50 > EMA200 and RSI < 30 and Volume > avg` |
| **PredictiveProphet** | BiLSTM AI Forecast | `prob > 0.52` then `conf = 0.95 + (prob - 0.52) * 0.4` |
| **HeikinBreakout** | Trend Breakout | `HeikinClose > HeikinOpen and MACD_hist > 0` |
| **VWAPScalperX** | VWAP + RSI Scalping | `price < VWAP and RSI < 30` |
| **RSIHeikinSniper** | RSI + Heikin‑Ashi Reversal | `RSI < 30 and HeikinClose > HeikinOpen` |
| **GapSniper** | Gap Momentum | `gap > 3% and close > open and volume > avg` |

Nightly the system can apply a capital boost based on agent ROI:

```python
for agent in agents:
    roi = agent.day_roi()
    if roi > 0.05 and agent.win_rate > 0.7:
        boost = 0.07
    elif roi > 0.03:
        boost = 0.03
    else:
        boost = 0
    agent.capital *= 1 + boost
```

This compounding loop is triggered automatically at 00:00 UTC each day.
