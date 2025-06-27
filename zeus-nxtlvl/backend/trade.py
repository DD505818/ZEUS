from loguru import logger


def execute_trade(symbol: str, amount: float) -> None:
    logger.info(f"Executing trade for {symbol} amount {amount}")
