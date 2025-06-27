import numpy as np
import pandas as pd
from .base import BaseAgent
from .utils import rsi

class VWAPScalperX(BaseAgent):
    def __init__(self, data):
        super().__init__()
        self.data = data.copy()

    def evaluate(self):
        prices = self.data['close'].values
        vols = self.data['volume'].values
        if len(prices) < 30:
            return None
        vwap = np.dot(prices[-30:], vols[-30:]) / max(vols[-30:].sum(), 1e-8)
        rs = rsi(pd.Series(prices[-14:])).iloc[-1]
        if prices[-1] < vwap and rs < 30:
            return {
                'signal': 'buy',
                'price': prices[-1],
                'confidence': 0.96,
                'reason': 'VWAP RSI scalp'
            }
        return None
