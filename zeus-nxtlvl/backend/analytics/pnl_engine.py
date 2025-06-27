import time
from loguru import logger


def run_pnl_loop(redis_url: str) -> None:
    logger.info("Starting PnL engine")
    while True:
        logger.debug("Computing PnL...")
        time.sleep(5)
