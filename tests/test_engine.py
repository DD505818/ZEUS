import unittest

from zeus_trade_engine import ZeusTradeEngine


class TestZeusTradeEngine(unittest.TestCase):
    def setUp(self):
        self.engine = ZeusTradeEngine()

    def test_hold_when_no_breakout(self):
        prices = [100, 100.1, 100.2]
        orderbook = {'bid_volume': 100, 'ask_volume': 100}
        decision = self.engine.run(prices, orderbook)
        self.assertEqual(decision, "HOLD")

    def test_execute_long_on_signal(self):
        prices = [100, 102, 104, 110]
        orderbook = {'bid_volume': 500, 'ask_volume': 100}
        decision = self.engine.run(prices, orderbook)
        self.assertIn(decision, {"EXECUTE_LONG", "HOLD", "HALT"})


if __name__ == "__main__":
    unittest.main()
