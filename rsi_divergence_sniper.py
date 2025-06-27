import numpy as np


def _compute_rsi(prices: np.ndarray, period: int) -> np.ndarray:
    """Simple RSI implementation to avoid external TA-Lib dependency."""
    prices = np.asarray(prices, dtype=float)
    if len(prices) <= period:
        return np.array([])
    deltas = np.diff(prices)
    seed = deltas[:period]
    up = seed[seed > 0].sum() / period
    down = -seed[seed < 0].sum() / period
    rs = up / down if down != 0 else float("inf")
    rsi_values = [100 - 100 / (1 + rs)]
    up_avg = up
    down_avg = down
    for delta in deltas[period:]:
        up_val = max(delta, 0)
        down_val = max(-delta, 0)
        up_avg = (up_avg * (period - 1) + up_val) / period
        down_avg = (down_avg * (period - 1) + down_val) / period
        rs = up_avg / down_avg if down_avg != 0 else float("inf")
        rsi_values.append(100 - 100 / (1 + rs))
    return np.array(rsi_values)


class RSIDivergenceSniper:
    def __init__(self, rsi_period: int = 14):
        self.rsi_period = rsi_period

    def detect_entry(self, prices) -> str | None:
        """Determine long/short entry based on RSI divergence."""
        if len(prices) < self.rsi_period + 1:
            return None
        rsi = _compute_rsi(np.array(prices), self.rsi_period)
        if rsi.size == 0:
            return None
        oversold = rsi[-1] < 30
        overbought = rsi[-1] > 70
        return "long" if oversold else "short" if overbought else None
