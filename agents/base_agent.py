from abc import ABC, abstractmethod
from typing import Any


class BaseAgent(ABC):
    """Abstract interface for ZEUS trading agents."""

    name: str = "BaseAgent"

    def __init__(self) -> None:
        self.capital: float = 0.0
        self.win_rate: float = 0.0

    def day_roi(self) -> float:
        """Return ROI for the current day."""
        return 0.0

    @abstractmethod
    def signal(self, *args: Any, **kwargs: Any):
        """Return trading signal."""
        raise NotImplementedError

    async def run(self) -> None:
        """Placeholder for async run loop."""
        pass
