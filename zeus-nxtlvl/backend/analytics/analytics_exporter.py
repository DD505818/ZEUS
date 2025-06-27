import os
import asyncio
import redis.asyncio as redis
from prometheus_client import start_http_server, Gauge

METRICS_PORT = int(os.getenv("METRICS_PORT", 9100))
REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379")

pnl_gauge = Gauge("zeus_pnl_latest", "Latest PnL value")


async def run_exporter() -> None:
    redis_client = redis.from_url(REDIS_URL)
    start_http_server(METRICS_PORT)
    while True:
        pnl = await redis_client.get("last_pnl")
        if pnl is not None:
            try:
                pnl_gauge.set(float(pnl))
            except ValueError:
                pnl_gauge.set(0.0)
        await asyncio.sleep(1)


if __name__ == "__main__":
    asyncio.run(run_exporter())
