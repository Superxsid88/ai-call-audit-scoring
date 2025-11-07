import os, json
from typing import Optional, Dict, Any

REDIS_URL = os.getenv("REDIS_URL")
_enabled = bool(REDIS_URL)

try:
    import redis.asyncio as redis  # type: ignore
    _r = redis.from_url(REDIS_URL) if _enabled else None
except Exception:
    _r = None
    _enabled = False

async def maybe_get_cache(key: str) -> Optional[Dict[str, Any]]:
    if not _enabled or _r is None:
        return None
    v = await _r.get(key)
    return json.loads(v) if v else None

async def maybe_set_cache(key: str, value: Dict[str, Any], ttl: int = 3600) -> None:
    if not _enabled or _r is None:
        return
    await _r.setex(key, ttl, json.dumps(value))
