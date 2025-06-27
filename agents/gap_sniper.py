import pandas as pd
from .base import BaseAgent

class GapSniper(BaseAgent):
    def __init__(self, data, gap_threshold=0.03):
        super().__init__()
        self.data = data.copy()
        self.gap_threshold = gap_threshold

    def detect_gap(self):
        prev_close = self.data['close'].shift(1)
        return (self.data['open'] - prev_close) / prev_close

    def evaluate(self):
        gap = self.detect_gap()
        volume = self.data['volume']
        breakout = self.data['close'] > self.data['open']
        if gap.iloc[-1] > self.gap_threshold and breakout.iloc[-1] and volume.iloc[-1] > volume.mean():
            return {
                'signal': 'buy',
                'price': self.data['close'].iloc[-1],
                'confidence': 0.93,
                'reason': 'Bullish breakaway gap'
            }
        elif gap.iloc[-1] < -self.gap_threshold and not breakout.iloc[-1] and volume.iloc[-1] > volume.mean():
            return {
                'signal': 'sell',
                'price': self.data['close'].iloc[-1],
                'confidence': 0.93,
                'reason': 'Bearish breakaway gap'
            }
        return None
