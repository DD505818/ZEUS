import pytest

from rsi_divergence_sniper import RSIDivergenceSniper
from momentum_killswitch import MomentumKillSwitch
from risk_sentinel import RiskSentinel
from zeus_trade_engine import ZeusTradeEngine


@pytest.fixture
def bullish_prices():
    return list(range(20))


@pytest.fixture
def bearish_prices():
    return list(range(20, 0, -1))


def test_rsi_divergence_sniper_long(bearish_prices):
    sniper = RSIDivergenceSniper(rsi_period=14)
    assert sniper.detect_entry(bearish_prices) == "long"


def test_rsi_divergence_sniper_short(bullish_prices):
    sniper = RSIDivergenceSniper(rsi_period=14)
    assert sniper.detect_entry(bullish_prices) == "short"


def test_momentum_killswitch():
    mk = MomentumKillSwitch(window=3)
    assert mk.should_exit([4, 3, 2, 1])
    assert not mk.should_exit([1, 2, 3, 4])


def test_risk_sentinel():
    sentinel = RiskSentinel(threshold=0.05)
    assert sentinel.detect_vol_spike([100, 106]) is True
    assert sentinel.detect_vol_spike([100, 102]) is False


def test_engine_run_executes(monkeypatch):
    engine = ZeusTradeEngine()
    engine.qb = type("QB", (), {"detect_breakout": lambda self, p, o: True})()
    engine.rsi = type("RSI", (), {"detect_entry": lambda self, p: "long"})()
    engine.momentum = type("MK", (), {"should_exit": lambda self, p: False})()
    engine.risk = type("Risk", (), {"detect_vol_spike": lambda self, p: False})()
    res = engine.run([1, 2], {"bid_volume": 2, "ask_volume": 1})
    assert res == "EXECUTE_LONG"


def test_engine_run_halt(monkeypatch):
    engine = ZeusTradeEngine()
    engine.risk = type("Risk", (), {"detect_vol_spike": lambda self, p: True})()
    res = engine.run([1, 2], {"bid_volume": 2, "ask_volume": 1})
    assert res == "HALT"


def test_engine_run_hold(monkeypatch):
    engine = ZeusTradeEngine()
    engine.qb = type("QB", (), {"detect_breakout": lambda self, p, o: True})()
    engine.rsi = type("RSI", (), {"detect_entry": lambda self, p: None})()
    engine.momentum = type("MK", (), {"should_exit": lambda self, p: False})()
    engine.risk = type("Risk", (), {"detect_vol_spike": lambda self, p: False})()
    res = engine.run([1, 2], {"bid_volume": 2, "ask_volume": 1})
    assert res == "HOLD"
