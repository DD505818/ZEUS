import os
import sys
import types
import numpy as np
import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# Provide a minimal talib implementation for tests
talib_mock = types.SimpleNamespace(RSI=lambda arr, timeperiod=14: np.zeros(len(arr)))
sys.modules.setdefault("talib", talib_mock)

from zeus_trade_engine import ZeusTradeEngine
from zeus_quantum_boost import QuantumBoost


def test_trade_engine_hold(monkeypatch):
    engine = ZeusTradeEngine()
    monkeypatch.setattr(engine.risk, "detect_vol_spike", lambda data: False)
    monkeypatch.setattr(engine.qb, "detect_breakout", lambda prices, ob: False)

    result = engine.run([100, 101], {"bid_volume": 1, "ask_volume": 1})
    assert result == "HOLD"


def test_trade_engine_execute_long(monkeypatch):
    engine = ZeusTradeEngine()
    monkeypatch.setattr(engine.risk, "detect_vol_spike", lambda data: False)
    monkeypatch.setattr(engine.qb, "detect_breakout", lambda prices, ob: True)
    monkeypatch.setattr(engine.rsi, "detect_entry", lambda prices: "long")
    monkeypatch.setattr(engine.momentum, "should_exit", lambda prices: False)

    result = engine.run([100, 102], {"bid_volume": 2, "ask_volume": 1})
    assert result == "EXECUTE_LONG"


def test_quantumboost_insufficient_price_data():
    qb = QuantumBoost()
    result = qb.detect_breakout([100], {"bid_volume": 1, "ask_volume": 1})
    assert result is False
