import unittest

from zeus_quantum_boost import QuantumBoost
from risk_sentinel import RiskSentinel


class TestQuantumBoost(unittest.TestCase):
    def setUp(self):
        self.qb = QuantumBoost(sensitivity=0.5)

    def test_no_breakout_with_insufficient_data(self):
        orderbook = {'bid_volume': 1, 'ask_volume': 1}
        self.assertFalse(self.qb.detect_breakout([100], orderbook))

    def test_breakout_detected(self):
        prices = [100, 102, 105]
        ob = {'bid_volume': 300, 'ask_volume': 100}
        self.assertTrue(self.qb.detect_breakout(prices, ob))


class TestRiskSentinel(unittest.TestCase):
    def setUp(self):
        self.risk = RiskSentinel(threshold=0.1)

    def test_no_spike_with_short_history(self):
        self.assertFalse(self.risk.detect_vol_spike([100]))

    def test_detect_spike(self):
        prices = [100, 120]
        self.assertTrue(self.risk.detect_vol_spike(prices))


if __name__ == "__main__":
    unittest.main()
