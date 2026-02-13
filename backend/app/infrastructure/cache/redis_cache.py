from __future__ import annotations

import json
from decimal import Decimal
from typing import Any

import redis.asyncio as redis

from app.config import settings


class DecimalEncoder(json.JSONEncoder):
    def default(self, o: Any) -> Any:
        if isinstance(o, Decimal):
            return str(o)
        return super().default(o)


class RedisCache:
    def __init__(self) -> None:
        self._redis: redis.Redis | None = None

    async def connect(self) -> None:
        if not settings.REDIS_URL:
            return
        try:
            self._redis = redis.from_url(settings.REDIS_URL, decode_responses=True)
            await self._redis.ping()
        except Exception:
            self._redis = None

    async def disconnect(self) -> None:
        if self._redis:
            await self._redis.close()

    async def get(self, key: str) -> Any | None:
        if not self._redis:
            return None
        value = await self._redis.get(key)
        if value is None:
            return None
        return json.loads(value)

    async def set(self, key: str, value: Any, ttl_seconds: int = 3600) -> None:
        if not self._redis:
            return
        serialized = json.dumps(value, cls=DecimalEncoder)
        await self._redis.set(key, serialized, ex=ttl_seconds)

    async def delete(self, key: str) -> None:
        if not self._redis:
            return
        await self._redis.delete(key)

    async def delete_pattern(self, pattern: str) -> None:
        if not self._redis:
            return
        async for key in self._redis.scan_iter(match=pattern):
            await self._redis.delete(key)


cache = RedisCache()
