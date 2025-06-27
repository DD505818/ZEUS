import pandas as pd
from .base import BaseAgent
from .utils import rsi, heikin_ashi

class RSIHeikinSniper(BaseAgent):
    def __init__(self, data):
        super().__init__()
        self.data = data.copy()

    def evaluate(self):
        if len(self.data) < 14:
            return None
        rsi_val = rsi(self.data['close'].tail(14)).iloc[-1]
        ha = heikin_ashi(self.data.tail(6))
        if rsi_val < 30 and ha['close'].iloc[-1] > ha['open'].iloc[-1]:
            return {
                'signal': 'buy',
                'price': self.data['close'].iloc[-1],
                'confidence': 0.94,
                'reason': 'RSI Heikin reversal'
            }
        return None
