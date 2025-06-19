
from zeus_quantum_boost import QuantumBoost
from rsi_divergence_sniper import RSIDivergenceSniper
from momentum_killswitch import MomentumKillSwitch
from risk_sentinel import RiskSentinel

class ZeusTradeEngine:
    def __init__(self):
        self.qb = QuantumBoost()
        self.rsi = RSIDivergenceSniper()
        self.momentum = MomentumKillSwitch()
        self.risk = RiskSentinel()

    def run(self, price_data, orderbook_data):
        if self.risk.detect_vol_spike(price_data):
            return "HALT"

        if self.qb.detect_breakout(price_data, orderbook_data):
            direction = self.rsi.detect_entry(price_data)
            if direction:
                if not self.momentum.should_exit(price_data):
                    return f"EXECUTE_{direction.upper()}"
        return "HOLD"
