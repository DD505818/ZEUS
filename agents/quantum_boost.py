import pandas as pd
from .base import BaseAgent
from .utils import rsi

class QuantumBoost(BaseAgent):
    def __init__(self, data):
        super().__init__()
        self.data = data.copy()

    def evaluate(self):
        df = self.data
        df['EMA50'] = df['close'].ewm(span=50, adjust=False).mean()
        df['EMA200'] = df['close'].ewm(span=200, adjust=False).mean()
        df['RSI'] = rsi(df['close'])
        if (
            df['EMA50'].iloc[-1] > df['EMA200'].iloc[-1]
            and df['RSI'].iloc[-1] < 30
            and df['volume'].iloc[-1] > df['volume'].rolling(20).mean().iloc[-1]
        ):
            return {
                'signal': 'buy',
                'price': df['close'].iloc[-1],
                'confidence': 0.95,
                'reason': 'EMA trend with RSI/volume'
            }
        return None
