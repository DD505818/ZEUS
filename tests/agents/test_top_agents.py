import os
import sys

import numpy as np
import pandas as pd

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
from backend.agents.top_agents import QuantumBoostAgent, GapSniperAgent


def test_quantum_boost_signal_shape():
    df = pd.DataFrame(
        {
            "close": np.linspace(1, 100, 250),
            "volume": np.linspace(100, 200, 250),
        }
    )
    action, conf = QuantumBoostAgent().signal(df)
    assert isinstance(action, str)
    assert isinstance(conf, float)


def test_gap_sniper_signal_shape():
    df = pd.DataFrame(
        {
            "open": [100, 104],
            "close": [100, 105],
            "volume": [50, 100],
        }
    )
    action, conf = GapSniperAgent().signal(df)
    assert isinstance(action, str)
    assert isinstance(conf, float)
