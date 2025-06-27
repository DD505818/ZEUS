
import numpy as np

class RSIDivergenceSniper:
    def __init__(self, rsi_period=14):
        self.rsi_period = rsi_period

    def _rsi(self, prices: np.ndarray) -> np.ndarray:
        deltas = np.diff(prices)
        seed = deltas[: self.rsi_period]
        up = seed[seed >= 0].sum() / self.rsi_period
        down = -seed[seed < 0].sum() / self.rsi_period
        rs = up / down if down != 0 else 0
        rsi = np.zeros_like(prices)
        rsi[: self.rsi_period] = 100 - 100 / (1 + rs)
        for i in range(self.rsi_period, len(prices)):
            delta = deltas[i - 1]
            upval = max(delta, 0)
            downval = -min(delta, 0)
            up = (up * (self.rsi_period - 1) + upval) / self.rsi_period
            down = (down * (self.rsi_period - 1) + downval) / self.rsi_period
            rs = up / down if down != 0 else 0
            rsi[i] = 100 - 100 / (1 + rs)
        return rsi

    def detect_entry(self, prices):
        prices = np.array(prices)
        if len(prices) < self.rsi_period + 1:
            return None
        rsi = self._rsi(prices)
        oversold = rsi[-1] < 30
        overbought = rsi[-1] > 70
        return "long" if oversold else "short" if overbought else None
