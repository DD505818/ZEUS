
import numpy as np

class MomentumKillSwitch:
    def __init__(self, window=5):
        self.window = window

    def should_exit(self, price_history):
        if len(price_history) < self.window:
            return False
        returns = np.diff(price_history[-self.window:])
        return np.sum(returns) < 0
