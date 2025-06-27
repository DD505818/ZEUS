
"""Risk management helpers."""


class RiskSentinel:
    """Detect sudden volatility spikes that warrant halting trading."""

    def __init__(self, threshold: float = 0.05) -> None:
        self.threshold = threshold

    def detect_vol_spike(self, price_data: list[float]) -> bool:
        """Return True if the latest price jump exceeds the threshold."""
        if len(price_data) < 2:
            return False
        prev_price = float(price_data[-2])
        if prev_price == 0:
            return False
        change = abs(float(price_data[-1]) - prev_price) / prev_price
        return change > self.threshold
