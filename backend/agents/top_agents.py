"""ZEUS\u00b0NXTLVL \u2014 Top 6 Agents & Capital Boost Logic."""

from __future__ import annotations

import asyncio
from datetime import datetime, timezone
from typing import Tuple, List

import numpy as np
import pandas as pd

from .base import AbstractAgent
from ..core.analytics import calc_ema, calc_rsi, calc_macd, heikin_ashi
from ..core.services import redis_pub


class QuantumBoostAgent(AbstractAgent):
    """High-momentum trend capture using EMA cross, RSI oversold and volume thrust."""

    name = "QuantumBoost"

    def signal(self, df: pd.DataFrame) -> Tuple[str, float]:
        ema50 = calc_ema(df["close"], 50)
        ema200 = calc_ema(df["close"], 200)
        rsi_val = calc_rsi(df["close"], 14).iloc[-1]
        vol_avg20 = df["volume"].rolling(20).mean().iloc[-1]
        if (
            ema50.iloc[-1] > ema200.iloc[-1]
            and rsi_val < 30
            and df["volume"].iloc[-1] > vol_avg20
        ):
            return "BUY", 0.95
        return "NONE", 0.0


class PredictiveProphetAgent(AbstractAgent):
    """Bi-LSTM micro-model producing probability of next-bar up-move."""

    name = "PredictiveProphet"

    def __init__(self, model_wrapper):
        super().__init__()
        self.model = model_wrapper

    def signal(self, features: np.ndarray, price: float) -> Tuple[str, float]:
        if features.shape[0] < 60:
            return "NONE", 0.0
        X = features[-60:].astype("float32").reshape(1, 60, 5)
        prob = float(self.model.predict(X))
        if prob > 0.52:
            conf = 0.95 + (prob - 0.52) * 0.4
            return "BUY", min(conf, 0.99)
        return "NONE", 0.0


class HeikinBreakoutAgent(AbstractAgent):
    """Heikin-Ashi candle breakout with MACD confirmation."""

    name = "HeikinBreakout"

    def signal(self, candles: pd.DataFrame) -> Tuple[str, float]:
        ha = heikin_ashi(candles.tail(6))
        macd_hist = calc_macd(candles["close"]).iloc[-1]
        if ha["close"].iloc[-1] > ha["open"].iloc[-1] and macd_hist > 0:
            conf = min(0.95 + macd_hist * 10, 0.98)
            return "BUY", conf
        return "NONE", 0.0


class VWAPScalperXAgent(AbstractAgent):
    """VWAP mean-reversion scalper (RSI oversold)."""

    name = "VWAPScalperX"

    def signal(self, prices: np.ndarray, vols: np.ndarray) -> Tuple[str, float]:
        if len(prices) < 30 or len(vols) < 30:
            return "NONE", 0.0
        vwap = np.dot(prices[-30:], vols[-30:]) / vols[-30:].sum()
        rs = calc_rsi(pd.Series(prices[-14:]), 14).iloc[-1]
        if prices[-1] < vwap and rs < 30:
            return "BUY", 0.96
        return "NONE", 0.0


class RSIHeikinSniperAgent(AbstractAgent):
    """Precision reversal agent using RSI + Heikin-Ashi."""

    name = "RSIHeikinSniper"

    def signal(self, df: pd.DataFrame) -> Tuple[str, float]:
        rsi_val = calc_rsi(df["close"], 14).iloc[-1]
        ha = heikin_ashi(df.tail(6))
        if rsi_val < 30 and ha["close"].iloc[-1] > ha["open"].iloc[-1]:
            return "BUY", 0.94
        return "NONE", 0.0


class GapSniperAgent(AbstractAgent):
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


def nightly_capital_boost(agents: List[AbstractAgent]):
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
        redis_pub("capital.patches", patches)


async def run_all_agents(agent_objs: List[AbstractAgent]):
    """Launch every agent concurrently."""
    async with asyncio.TaskGroup() as tg:
        for agent in agent_objs:
            tg.create_task(agent.run())


def bootstrap_agents(model_wrapper) -> List[AbstractAgent]:
    """Initialise all six agents with required dependencies."""
    return [
        QuantumBoostAgent(),
        PredictiveProphetAgent(model_wrapper),
        HeikinBreakoutAgent(),
        VWAPScalperXAgent(),
        RSIHeikinSniperAgent(),
        GapSniperAgent(),
    ]
