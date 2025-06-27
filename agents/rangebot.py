import pandas as pd

class RangeBot:
    def __init__(self, data, bb_window=20, atr_window=14):
        self.data = data.copy()
        self.bb_window = bb_window
        self.atr_window = atr_window

    def bollinger_bands(self):
        price = self.data['close']
        sma = price.rolling(self.bb_window).mean()
        std = price.rolling(self.bb_window).std()
        upper = sma + (2 * std)
        lower = sma - (2 * std)
        return upper, lower

    def average_true_range(self):
        high = self.data['high']
        low = self.data['low']
        close = self.data['close']
        tr = pd.concat([
            high - low,
            (high - close.shift()).abs(),
            (low - close.shift()).abs()
        ], axis=1).max(axis=1)
        atr = tr.rolling(self.atr_window).mean()
        return atr

    def generate_signal(self):
        upper, lower = self.bollinger_bands()
        atr = self.average_true_range()
        close = self.data['close']

        if close.iloc[-1] < lower.iloc[-1]:
            return {'signal': 'buy', 'price': close.iloc[-1], 'reason': 'Below lower Bollinger Band'}
        elif close.iloc[-1] > upper.iloc[-1]:
            return {'signal': 'sell', 'price': close.iloc[-1], 'reason': 'Above upper Bollinger Band'}
        return None
