import sys
import os
import types
import numpy as np
import pytest

# Create a minimal talib stub so zeus modules import correctly
stub_talib = types.ModuleType('talib')

def _rsi(prices, timeperiod=14):
    # Return neutral RSI values to avoid triggering overbought/oversold
    return np.array([50] * len(prices))

stub_talib.RSI = _rsi
sys.modules.setdefault('talib', stub_talib)

# Ensure project root is on path for test discovery
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from zeus_trade_engine import ZeusTradeEngine
from zeus_quantum_boost import QuantumBoost


def test_trade_engine_hold(monkeypatch):
    engine = ZeusTradeEngine()

    # Force breakout detection to be false
    monkeypatch.setattr(engine.qb, 'detect_breakout', lambda *args, **kwargs: False)
    monkeypatch.setattr(engine.risk, 'detect_vol_spike', lambda *args, **kwargs: False)

    result = engine.run([1, 1.02], {'bid_volume': 1, 'ask_volume': 1})
    assert result == 'HOLD'


def test_trade_engine_execute_long(monkeypatch):
    engine = ZeusTradeEngine()

    monkeypatch.setattr(engine.risk, 'detect_vol_spike', lambda *args, **kwargs: False)
    monkeypatch.setattr(engine.qb, 'detect_breakout', lambda *args, **kwargs: True)
    monkeypatch.setattr(engine.rsi, 'detect_entry', lambda *args, **kwargs: 'long')
    monkeypatch.setattr(engine.momentum, 'should_exit', lambda *args, **kwargs: False)

    result = engine.run([1, 1.1], {'bid_volume': 2, 'ask_volume': 1})
    assert result == 'EXECUTE_LONG'


def test_quantumboost_insufficient_data():
    qb = QuantumBoost()
    result = qb.detect_breakout([100], {'bid_volume': 1, 'ask_volume': 1})
    assert result is False
