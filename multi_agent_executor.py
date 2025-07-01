# multi_agent_executor.py
# ZEUS°NXTLVL Multi-Agent Execution Engine (Modular)

import pandas as pd
from datetime import datetime
from agents import (
    QuantumBoost,
    PredictiveProphet,
    HeikinBreakout,
    VWAPScalperX,
    RSIHeikinSniper,
    GapSniper,
)

class Broker:
    def execute_trade(self, symbol, signal_type, price):
        print(f"[BROKER] Executing {signal_type.upper()} on {symbol} at ${price}")
        return {
            "symbol": symbol,
            "side": signal_type,
            "executed_price": price,
            "timestamp": datetime.utcnow().isoformat(),
        }

class MultiAgentExecutor:
    CONFIDENCE_GATE = 0.95

    def __init__(self, symbol, market_data):
        self.symbol = symbol
        self.data = market_data
        self.results = []
        self.broker = Broker()

        # instantiate agents
        self.agents = {
            "QuantumBoost": QuantumBoost(self.data),
            "PredictiveProphet": PredictiveProphet(self.data),
            "HeikinBreakout": HeikinBreakout(self.data),
            "VWAPScalperX": VWAPScalperX(self.data),
            "RSIHeikinSniper": RSIHeikinSniper(self.data),
            "GapSniper": GapSniper(self.data),
        }

    def run_all(self, timestamp):
        signals = []
        for name, agent in self.agents.items():
            result = agent.evaluate()
            if result and result.get("confidence", 1.0) >= self.CONFIDENCE_GATE:
                result.update({"agent": name, "time": timestamp})
                self.broker.execute_trade(self.symbol, result["signal"], result["price"])
                signals.append(result)
        self.results.extend(signals)
        return signals

    def nightly_update(self):
        """Adjust agent capital allocations based on daily performance."""
        for agent in self.agents.values():
            roi = agent.day_roi()
            if roi > 0.04 and agent.win_rate > 0.85:
                boost = 0.07
            elif roi > 0.03:
                boost = 0.03
            elif roi < -0.02:
                boost = -0.05
            else:
                boost = 0

            agent.capital *= 1 + boost
            agent.trade_history.clear()
            agent.wins = agent.losses = 0

    def summary(self):
        return pd.DataFrame(self.results)
