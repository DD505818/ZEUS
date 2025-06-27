
import numpy as np


class QuantumBoost:
    def __init__(self, sensitivity: float = 0.9) -> None:
        self.sensitivity = sensitivity

    def detect_breakout(self, price_data, orderbook_data) -> bool:
        if len(price_data) < 2:
            return False
        price_velocity = float(np.gradient(price_data)[-1])
        ask = float(orderbook_data.get("ask_volume", 0))
        bid = float(orderbook_data.get("bid_volume", 0))
        if ask <= 0:
            return False
        volume_ratio = bid / (ask + 1e-8)
        signal = price_velocity * volume_ratio
        return signal > self.sensitivity
