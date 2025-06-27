
import numpy as np


class MomentumKillSwitch:
    """Detect prolonged negative momentum."""

    def __init__(self, window: int = 5) -> None:
        self.window = window

    def should_exit(self, price_history: list[float]) -> bool:
        """Return True when recent returns show downward momentum."""
        if len(price_history) < self.window:
            return False
        history_arr = np.array(price_history[-self.window:], dtype=float)
        returns = np.diff(history_arr)
        return np.sum(returns) < 0
