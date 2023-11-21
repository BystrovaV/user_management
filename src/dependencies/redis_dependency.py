from fastapi import Depends
from redis.asyncio.client import Pipeline

from adapters.orm_engines.redis_engine import Redis
from core.settings import Settings


class RedisDependency:
    def __init__(self):
        self.redis = None

    def __call__(self) -> Redis:
        settings = Settings()
        self.redis = (
            Redis.start(settings.get_redis_url) if not self.redis else self.redis
        )
        return self.redis


get_redis_dependency = RedisDependency()


async def get_redis_connection(
    redis_base: Redis = Depends(get_redis_dependency),
) -> Pipeline:
    async with redis_base.session_maker.pipeline() as session:
        yield session
