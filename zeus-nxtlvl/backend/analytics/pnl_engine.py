import os
import asyncio
import redis.asyncio as redis

REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379")

class PnLEngine:
    """Async PnL engine that stores results in Redis."""

    def __init__(self):
        self.redis = redis.from_url(REDIS_URL)

    async def calculate_pnl(self) -> float:
        """Placeholder for actual PnL calculation."""
        pnl = 0.0
        await self.redis.set("last_pnl", pnl)
        return pnl

    async def run(self) -> None:
        while True:
            await self.calculate_pnl()
            await asyncio.sleep(1)


if __name__ == "__main__":
    asyncio.run(PnLEngine().run())
