

class RiskSentinel:
    def __init__(self, threshold=0.05):
        self.threshold = threshold

    def detect_vol_spike(self, price_data):
        if len(price_data) < 2:
            return False
        change = abs(price_data[-1] - price_data[-2]) / price_data[-2]
        return change > self.threshold
