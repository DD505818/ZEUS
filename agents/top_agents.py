"""Top trading agents and nightly capital booster."""

from __future__ import annotations

import asyncio
from datetime import datetime, timezone
from typing import List, Tuple

import numpy as np
import pandas as pd

from .base_agent import BaseAgent


# ---------------------------------------------------------------------------
# Agent classes
# ---------------------------------------------------------------------------


class QuantumBoostAgent(BaseAgent):
    """High-momentum trend capture using EMA cross, RSI and volume."""

    name = "QuantumBoost"

    def signal(self, df: pd.DataFrame) -> Tuple[str, float]:
        ema50 = df["close"].ewm(span=50, adjust=False).mean()
        ema200 = df["close"].ewm(span=200, adjust=False).mean()
        rsi = df["close"].diff().clip(lower=0).rolling(14).mean()
        rsi_loss = -df["close"].diff().clip(upper=0).rolling(14).mean()
        rs = rsi / rsi_loss
        rsi_val = 100 - (100 / (1 + rs))
        vol_avg20 = df["volume"].rolling(20).mean()
        if (
            ema50.iloc[-1] > ema200.iloc[-1]
            and rsi_val.iloc[-1] < 30
            and df["volume"].iloc[-1] > vol_avg20.iloc[-1]
        ):
            return "BUY", 0.95
        return "NONE", 0.0


class PredictiveProphetAgent(BaseAgent):
    """Bi-LSTM micro-model producing probability of next-bar up-move."""

    name = "PredictiveProphet"

    def __init__(self, model_wrapper) -> None:
        super().__init__()
        self.model = model_wrapper

    def signal(self, features: np.ndarray, price: float) -> Tuple[str, float]:
        X = features[-60:].astype("float32").reshape(1, 60, 5)
        prob = float(self.model.predict(X))
        if prob > 0.52:
            conf = 0.95 + (prob - 0.52) * 0.4
            return "BUY", min(conf, 0.99)
        return "NONE", 0.0


class HeikinBreakoutAgent(BaseAgent):
    """Heikin-Ashi candle breakout with MACD confirmation."""

    name = "HeikinBreakout"

    def signal(self, candles: pd.DataFrame) -> Tuple[str, float]:
        ha_close = (
            candles["open"] + candles["high"] + candles["low"] + candles["close"]
        ) / 4
        ha_open = ((candles["open"].shift() + candles["close"].shift()) / 2).fillna(
            candles["open"]
        )
        ha = pd.DataFrame({"open": ha_open, "close": ha_close})
        macd_line = (
            candles["close"].ewm(span=12, adjust=False).mean()
            - candles["close"].ewm(span=26, adjust=False).mean()
        )
        macd_signal = macd_line.ewm(span=9, adjust=False).mean()
        macd_hist = macd_line - macd_signal
        if ha["close"].iloc[-1] > ha["open"].iloc[-1] and macd_hist.iloc[-1] > 0:
            conf = min(0.95 + macd_hist.iloc[-1] * 10, 0.98)
            return "BUY", conf
        return "NONE", 0.0


class VWAPScalperXAgent(BaseAgent):
    """VWAP mean-reversion scalper."""

    name = "VWAPScalperX"

    def signal(self, prices: np.ndarray, vols: np.ndarray) -> Tuple[str, float]:
        if len(prices) < 30 or len(vols) < 30:
            return "NONE", 0.0
        vwap = float(np.dot(prices[-30:], vols[-30:]) / np.sum(vols[-30:]))
        gains = np.diff(prices[-14:]).clip(min=0).mean()
        losses = -np.diff(prices[-14:]).clip(max=0).mean()
        rs = gains / (losses + 1e-8)
        rsi_val = 100 - (100 / (1 + rs))
        if prices[-1] < vwap and rsi_val < 30:
            return "BUY", 0.96
        return "NONE", 0.0


class RSIHeikinSniperAgent(BaseAgent):
    """Precision reversal agent using RSI + Heikin-Ashi."""

    name = "RSIHeikinSniper"

    def signal(self, df: pd.DataFrame) -> Tuple[str, float]:
        gains = df["close"].diff().clip(lower=0).rolling(14).mean()
        losses = -df["close"].diff().clip(upper=0).rolling(14).mean()
        rs = gains / (losses + 1e-8)
        rsi_val = 100 - (100 / (1 + rs))
        ha_close = (df["open"] + df["high"] + df["low"] + df["close"]) / 4
        ha_open = ((df["open"].shift() + df["close"].shift()) / 2).fillna(df["open"])
        if rsi_val.iloc[-1] < 30 and ha_close.iloc[-1] > ha_open.iloc[-1]:
            return "BUY", 0.94
        return "NONE", 0.0


class GapSniperAgent(BaseAgent):
    """Open-range breakout after gap-up > 3%."""

    name = "GapSniper"

    def signal(self, df: pd.DataFrame) -> Tuple[str, float]:
        prev_close = df["close"].shift(1)
        gap = (df["open"] - prev_close) / prev_close
        if (
            gap.iloc[-1] > 0.03
            and df["close"].iloc[-1] > df["open"].iloc[-1]
            and df["volume"].iloc[-1] > df["volume"].mean()
        ):
            return "BUY", 0.93
        return "NONE", 0.0


# ---------------------------------------------------------------------------
# Capital boost compounder
# ---------------------------------------------------------------------------


def nightly_capital_boost(agents: List[BaseAgent]) -> None:
    """Apply dynamic equity injection at 00:00 UTC."""

    patches = []
    for agent in agents:
        roi = agent.day_roi()
        if roi > 0.05 and agent.win_rate > 0.7:
            boost = 0.07
        elif roi > 0.03:
            boost = 0.03
        else:
            boost = 0.0
        if boost:
            original = agent.capital
            agent.capital *= 1 + boost
            patches.append(
                {
                    "agent": agent.name,
                    "op": "replace",
                    "path": "/capital",
                    "value": agent.capital,
                    "prev": original,
                    "timestamp": datetime.now(timezone.utc).isoformat(),
                }
            )
    if patches:
        try:
            from redis import Redis

            client = Redis()
            client.publish("capital.patches", str(patches))
        except Exception:
            pass


# ---------------------------------------------------------------------------
# Async agent driver
# ---------------------------------------------------------------------------


async def run_all_agents(agent_objs: List[BaseAgent]) -> None:
    """Launch every agent concurrently."""

    async with asyncio.TaskGroup() as tg:
        for agent in agent_objs:
            tg.create_task(agent.run())


def bootstrap_agents(model_wrapper) -> List[BaseAgent]:
    """Factory to initialise all six agents with required deps."""

    return [
        QuantumBoostAgent(),
        PredictiveProphetAgent(model_wrapper),
        HeikinBreakoutAgent(),
        VWAPScalperXAgent(),
        RSIHeikinSniperAgent(),
        GapSniperAgent(),
    ]
