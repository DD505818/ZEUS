from __future__ import annotations

from typing import Dict, Type

from ..agents.top_agents import (
    QuantumBoostAgent,
    PredictiveProphetAgent,
    HeikinBreakoutAgent,
    VWAPScalperXAgent,
    RSIHeikinSniperAgent,
    GapSniperAgent,
)
from ..agents.base import AbstractAgent


# Registry mapping agent names to their class objects
strategy_registry: Dict[str, Type[AbstractAgent]] = {
    "QuantumBoost": QuantumBoostAgent,
    "PredictiveProphet": PredictiveProphetAgent,
    "HeikinBreakout": HeikinBreakoutAgent,
    "VWAPScalperX": VWAPScalperXAgent,
    "RSIHeikinSniper": RSIHeikinSniperAgent,
    "GapSniper": GapSniperAgent,
}


def get_agent(name: str, *args, **kwargs) -> AbstractAgent:
    """Instantiate an agent by name using the registry."""
    cls = strategy_registry[name]
    return cls(*args, **kwargs)
