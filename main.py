from zeus_trade_engine import ZeusTradeEngine
import time
import numpy as np
import logging
import signal
import sys

# Configure logging to output to console and a log file
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler("logs/zeus.log"),
    ],
)

logger = logging.getLogger(__name__)

engine = ZeusTradeEngine()

price_data = []
orderbook_data = {"bid_volume": 0, "ask_volume": 0}


def fetch_data():
    return [100 + np.random.randn()], {"bid_volume": 500, "ask_volume": 480}


running = True


def shutdown(signum, frame):
    global running
    logger.info("Shutdown signal received. Exiting...")
    running = False


signal.signal(signal.SIGINT, shutdown)
signal.signal(signal.SIGTERM, shutdown)

try:
    while running:
        price, ob = fetch_data()
        price_data.extend(price)
        orderbook_data.update(ob)

        decision = engine.run(price_data, orderbook_data)
        logger.info("[ZEUS] Decision: %s", decision)
        time.sleep(1)
except KeyboardInterrupt:
    logger.info("Keyboard interrupt received. Exiting...")
