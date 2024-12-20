import redis.asyncio as redis

class RedisConnector:
    def __init__(self, host: str, port: int):
        self._host = host
        self._port = port
        self._redis = None

    async def connect(self):
        self._redis = await redis.Redis(host=self._host, port=self._port)

    async def set(self, key: str, value: str, expire: int = None):
        if not self._redis:
            raise ConnectionError("Redis connection is not established.")
        if expire:
            await self._redis.set(key, value, ex=expire)
        else:
            await self._redis.set(key, value)

    async def get(self, key: str):
        if not self._redis:
            raise ConnectionError("Redis connection is not established.")
        return await self._redis.get(key)

    async def delete(self, key: str):
        if not self._redis:
            raise ConnectionError("Redis connection is not established.")
        await self._redis.delete(key)

    async def close(self):
        if self._redis:
            await self._redis.close()
