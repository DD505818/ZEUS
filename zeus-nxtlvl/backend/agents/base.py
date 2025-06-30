class BaseAgent:
    """Base trading agent."""

    def run(self, prices: list[float]) -> str:
        raise NotImplementedError
