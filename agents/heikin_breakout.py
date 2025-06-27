import pandas as pd
from .base import BaseAgent
from .utils import heikin_ashi, macd

class HeikinBreakout(BaseAgent):
    def __init__(self, data):
        super().__init__()
        self.data = data.copy()

    def evaluate(self):
        if len(self.data) < 6:
            return None
        ha = heikin_ashi(self.data.tail(6))
        macd_hist = macd(self.data['close']).iloc[-1]
        if ha['close'].iloc[-1] > ha['open'].iloc[-1] and macd_hist > 0:
            conf = min(0.95 + macd_hist * 10, 0.98)
            return {
                'signal': 'buy',
                'price': self.data['close'].iloc[-1],
                'confidence': conf,
                'reason': 'Heikin breakout'
            }
        return None
