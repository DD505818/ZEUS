import numpy as np
import pandas as pd

from agents.top_agents import (
    QuantumBoostAgent,
    HeikinBreakoutAgent,
    VWAPScalperXAgent,
    RSIHeikinSniperAgent,
    GapSniperAgent,
)


def test_quantum_boost_signal():
    data = pd.DataFrame(
        {
            "close": np.linspace(1, 250, 250),
            "volume": np.ones(250) * 1000,
        }
    )
    agent = QuantumBoostAgent()
    action, conf = agent.signal(data)
    assert isinstance(action, str)
    assert isinstance(conf, float)


def test_heikin_breakout_signal():
    candles = pd.DataFrame(
        {
            "open": np.arange(10, 16),
            "high": np.arange(11, 17),
            "low": np.arange(9, 15),
            "close": np.arange(10, 16) + 0.5,
        }
    )
    agent = HeikinBreakoutAgent()
    action, conf = agent.signal(candles)
    assert isinstance(action, str)
    assert isinstance(conf, float)


def test_vwap_scalper_signal():
    prices = np.linspace(1, 50, 50)
    vols = np.ones(50) * 10
    agent = VWAPScalperXAgent()
    action, conf = agent.signal(prices, vols)
    assert isinstance(action, str)
    assert isinstance(conf, float)


def test_rsi_heikin_sniper_signal():
    df = pd.DataFrame(
        {
            "open": np.arange(20),
            "high": np.arange(1, 21),
            "low": np.arange(0, 20),
            "close": np.arange(20),
        }
    )
    agent = RSIHeikinSniperAgent()
    action, conf = agent.signal(df)
    assert isinstance(action, str)
    assert isinstance(conf, float)


def test_gap_sniper_signal():
    df = pd.DataFrame(
        {
            "open": [103, 106, 110],
            "close": [100, 108, 112],
            "volume": [5000, 6000, 7000],
        }
    )
    agent = GapSniperAgent()
    action, conf = agent.signal(df)
    assert isinstance(action, str)
    assert isinstance(conf, float)
