import types
import os, sys
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
import pytest
if "talib" not in sys.modules:
    talib_stub = types.ModuleType("talib")
    def RSI(arr, timeperiod=14):
        import numpy as np
        return np.array([50]*len(arr))
    talib_stub.RSI = RSI
    sys.modules["talib"] = talib_stub


from zeus_trade_engine import ZeusTradeEngine
from zeus_quantum_boost import QuantumBoost


def test_run_hold(monkeypatch):
    engine = ZeusTradeEngine()

    monkeypatch.setattr(engine.qb, "detect_breakout", lambda price, order: False)
    monkeypatch.setattr(engine.rsi, "detect_entry", lambda price: None)
    monkeypatch.setattr(engine.momentum, "should_exit", lambda price: False)
    monkeypatch.setattr(engine.risk, "detect_vol_spike", lambda price: False)

    result = engine.run([1, 2, 3], {"bid_volume": 100, "ask_volume": 100})
    assert result == "HOLD"


def test_run_execute_long(monkeypatch):
    engine = ZeusTradeEngine()

    monkeypatch.setattr(engine.qb, "detect_breakout", lambda price, order: True)
    monkeypatch.setattr(engine.rsi, "detect_entry", lambda price: "long")
    monkeypatch.setattr(engine.momentum, "should_exit", lambda price: False)
    monkeypatch.setattr(engine.risk, "detect_vol_spike", lambda price: False)

    result = engine.run([1, 2, 3, 4], {"bid_volume": 200, "ask_volume": 50})
    assert result == "EXECUTE_LONG"


def test_quantumboost_insufficient_data():
    qb = QuantumBoost()
    result = qb.detect_breakout([100], {"bid_volume": 10, "ask_volume": 5})
    assert result is False
