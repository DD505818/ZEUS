class BaseAgent:
    """Base class for trading agents."""

    def run(self):
        raise NotImplementedError("Agents must implement the run method")
