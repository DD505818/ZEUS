
from zeus_trade_engine import ZeusTradeEngine
import time
import numpy as np


engine = ZeusTradeEngine()

price_data = []
orderbook_data = {"bid_volume": 0, "ask_volume": 0}


def fetch_data():
    return [100 + np.random.randn()], {"bid_volume": 500, "ask_volume": 480}


def main() -> None:
    """Run a tiny trading demo that prints decisions indefinitely."""
    while True:
        price, ob = fetch_data()
        price_data.extend(price)
        orderbook_data.update(ob)

        decision = engine.run(price_data, orderbook_data)
        print(f"[ZEUS] Decision: {decision}")
        time.sleep(1)


if __name__ == "__main__":
    main()
