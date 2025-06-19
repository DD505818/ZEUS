
import talib
import numpy as np

class RSIDivergenceSniper:
    def __init__(self, rsi_period=14):
        self.rsi_period = rsi_period

    def detect_entry(self, prices):
        rsi = talib.RSI(np.array(prices), timeperiod=self.rsi_period)
        oversold = rsi[-1] < 30
        overbought = rsi[-1] > 70
        return "long" if oversold else "short" if overbought else None
