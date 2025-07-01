
from zeus_quantum_boost import QuantumBoost
from rsi_divergence_sniper import RSIDivergenceSniper
from momentum_killswitch import MomentumKillSwitch
from risk_sentinel import RiskSentinel
from nxtlvl import (
    QuantumBoostAgent,
    PredictiveProphet,
    HeikinBreakout,
    VWAPScalperX,
    RSIHeikinSniper,
    GapSniper,
    CapitalBooster,
)

class ZeusTradeEngine:
    def __init__(self):
        self.qb = QuantumBoost()
        self.rsi = RSIDivergenceSniper()
        self.momentum = MomentumKillSwitch()
        self.risk = RiskSentinel()
        self.agents = [
            QuantumBoostAgent(),
            HeikinBreakout(),
            VWAPScalperX(),
            RSIHeikinSniper(),
            GapSniper(),
        ]
        # PredictiveProphet requires model and scaler; user should initialize separately
        self.booster = CapitalBooster()

    def run(self, price_data, orderbook_data):
        if self.risk.detect_vol_spike(price_data):
            return "HALT"

        if self.qb.detect_breakout(price_data, orderbook_data):
            direction = self.rsi.detect_entry(price_data)
            if direction:
                if not self.momentum.should_exit(price_data):
                    return f"EXECUTE_{direction.upper()}"
        return "HOLD"

    def generate_signals(self, df, **kwargs):
        results = {}
        for agent in self.agents:
            if isinstance(agent, PredictiveProphet):
                features = kwargs.get('features')
                price = kwargs.get('price')
                if features is None or price is None:
                    continue
                results[agent.__class__.__name__] = agent.signal(features, price)
            elif isinstance(agent, VWAPScalperX):
                prices = kwargs.get('prices')
                vols = kwargs.get('vols')
                if prices is None or vols is None:
                    continue
                results[agent.__class__.__name__] = agent.signal(prices, vols)
            else:
                results[agent.__class__.__name__] = agent.signal(df)
        return results

    def nightly_boost(self):
        self.booster.apply(self.agents)
