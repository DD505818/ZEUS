
import numpy as np


def _calc_rsi(prices: np.ndarray, period: int) -> np.ndarray:
    """Simple RSI implementation to avoid heavy external dependencies."""
    deltas = np.diff(prices)
    seed = deltas[:period]
    up = seed[seed >= 0].sum() / period
    down = -seed[seed < 0].sum() / period
    rs = up / down if down != 0 else 0
    rsi = np.zeros_like(prices)
    rsi[:period] = 100.0 - 100.0 / (1.0 + rs)

    for i in range(period, len(prices)):
        delta = deltas[i - 1]
        if delta > 0:
            up_val = delta
            down_val = 0
        else:
            up_val = 0
            down_val = -delta
        up = (up * (period - 1) + up_val) / period
        down = (down * (period - 1) + down_val) / period
        rs = up / down if down != 0 else 0
        rsi[i] = 100.0 - 100.0 / (1.0 + rs)

    return rsi


class RSIDivergenceSniper:
    def __init__(self, rsi_period: int = 14):
        self.rsi_period = rsi_period

    def detect_entry(self, prices):
        prices_arr = np.array(prices, dtype=float)
        if len(prices_arr) < self.rsi_period:
            return None
        rsi = _calc_rsi(prices_arr, self.rsi_period)
        oversold = rsi[-1] < 30
        overbought = rsi[-1] > 70
        return "long" if oversold else "short" if overbought else None
