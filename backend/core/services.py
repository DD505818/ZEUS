import json
from typing import Any


def redis_pub(channel: str, message: Any) -> None:
    """Stub for publishing a message to Redis."""
    print(f"[redis] publish to {channel}: {json.dumps(message)}")
