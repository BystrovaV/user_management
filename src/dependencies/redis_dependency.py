import redis.asyncio as redis
from fastapi import Depends
from redis.asyncio import ConnectionPool


class RedisDependency:
    def __init__(self):
        self.connection_pool = None

    def __call__(self) -> ConnectionPool:
        self.connection_pool = (
            redis.ConnectionPool.from_url("redis://localhost:6379")
            if not self.connection_pool
            else self.connection_pool
        )
        return self.connection_pool


get_redis_dependency = RedisDependency()


async def get_redis_connection(
    redis: ConnectionPool = Depends(get_redis_dependency),
) -> ConnectionPool:
    return redis
