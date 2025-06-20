
import numpy as np

class QuantumBoost:
    def __init__(self, sensitivity=0.9):
        self.sensitivity = sensitivity

    def detect_breakout(self, price_data, orderbook_data):
        """Detect a breakout using recent price and order book information."""

        # np.gradient requires at least two price points; otherwise a breakout
        # cannot be determined reliably. In such cases we return False rather
        # than raising an exception.
        if len(price_data) < 2:
            return False

        price_velocity = np.gradient(price_data)[-1]
        volume_ratio = orderbook_data['bid_volume'] / (
            orderbook_data['ask_volume'] + 1e-8
        )
        signal = price_velocity * volume_ratio
        return signal > self.sensitivity
