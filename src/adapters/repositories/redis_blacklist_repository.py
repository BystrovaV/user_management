import redis.asyncio as redis
from redis.asyncio import ConnectionPool

from ports.repositories.blacklist_repository import BlacklistRepository


class RedisBlacklistRepository(BlacklistRepository):
    def __init__(self, pool: ConnectionPool):
        self.pool = pool

    async def add(self, token: str, token_exp: int):
        client = redis.Redis(connection_pool=self.pool)
        await client.set("bl_" + token, token)
        await client.expireat("bl_" + token, token_exp)
        await client.aclose()

    async def check(self, token: str) -> bool:
        client = redis.Redis(connection_pool=self.pool)
        token = await client.get("bl_" + token)
        print(token)
        await client.aclose()

        if not token:
            return False
        return True
