import sqlite3
import time
import numpy as np
from zeus_trade_engine import ZeusTradeEngine


class MultiAgentExecutor:
    """Simple executor managing trading engine interactions."""

    def __init__(self):
        self.engine = ZeusTradeEngine()
        # In lieu of a real message bus, use an in-memory SQLite DB
        self.conn = sqlite3.connect(":memory:")

    def fetch_data(self):
        """Mock price and order book data."""
        return [100 + np.random.randn()], {"bid_volume": 500, "ask_volume": 480}

    def run(self, iterations=10):
        """Run a loop of trading decisions."""
        price_data = []
        orderbook_data = {"bid_volume": 0, "ask_volume": 0}
        for _ in range(iterations):
            price, ob = self.fetch_data()
            price_data.extend(price)
            orderbook_data.update(ob)
            if len(price_data) < 2:
                continue
            decision = self.engine.run(price_data, orderbook_data)
            print(f"[ZEUS] Decision: {decision}")
            time.sleep(1)

    def close(self):
        """Close internal resources."""
        if self.conn is not None:
            self.conn.close()
            self.conn = None
