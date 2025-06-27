class AbstractAgent:
    """Base class for all trading agents."""

    name: str = ""

    def __init__(self) -> None:
        self.capital = 0.0
        self.win_rate = 0.0

    # ------------------------------------------------------------------
    # Generic stats helpers
    # ------------------------------------------------------------------
    def day_roi(self) -> float:
        """Return ROI for the current day."""
        return 0.0

    # ------------------------------------------------------------------
    # Required trading interface
    # ------------------------------------------------------------------
    def analyze_market(self, data):
        """Analyse raw market data and return a processed form."""
        return data

    def generate_signal(self, data):
        """Return a trading signal as (action, confidence)."""
        if hasattr(self, "signal"):
            return self.signal(data)
        raise NotImplementedError("generate_signal must be implemented")

    async def execute_trade(self, signal, portfolio=None) -> None:
        """Execute a trade based on the signal."""
        return None

    async def run(self, market_data=None, portfolio=None) -> None:
        """High-level execution loop for live trading."""
        processed = self.analyze_market(market_data)
        signal = self.generate_signal(processed)
        await self.execute_trade(signal, portfolio)
