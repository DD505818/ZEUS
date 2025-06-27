class AbstractAgent:
    """Base class for all trading agents."""

    name: str = ""

    def __init__(self):
        self.capital = 0.0
        self.win_rate = 0.0

    def day_roi(self) -> float:
        """Return ROI for the current day."""
        return 0.0

    async def run(self):
        pass
