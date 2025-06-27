import os
import sys
import types
import pytest

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

# Provide a minimal fake 'talib' module for tests
talib_stub = types.ModuleType("talib")
talib_stub.RSI = lambda data, timeperiod=14: [50 for _ in data]
sys.modules.setdefault("talib", talib_stub)

from zeus_trade_engine import ZeusTradeEngine
from zeus_quantum_boost import QuantumBoost


def test_run_hold(monkeypatch):
    engine = ZeusTradeEngine()
    monkeypatch.setattr(engine.risk, "detect_vol_spike", lambda data: False)
    monkeypatch.setattr(engine.qb, "detect_breakout", lambda price, orderbook: False)
    result = engine.run([100, 101, 102], {"bid_volume": 5, "ask_volume": 5})
    assert result == "HOLD"


def test_run_execute_long(monkeypatch):
    engine = ZeusTradeEngine()
    monkeypatch.setattr(engine.risk, "detect_vol_spike", lambda data: False)
    monkeypatch.setattr(engine.qb, "detect_breakout", lambda price, orderbook: True)
    monkeypatch.setattr(engine.rsi, "detect_entry", lambda price: "long")
    monkeypatch.setattr(engine.momentum, "should_exit", lambda price: False)
    result = engine.run([100, 101, 102], {"bid_volume": 10, "ask_volume": 5})
    assert result == "EXECUTE_LONG"


def test_quantumboost_insufficient_data():
    qb = QuantumBoost()
    result = qb.detect_breakout([100], {"bid_volume": 1, "ask_volume": 1})
    assert result is False

