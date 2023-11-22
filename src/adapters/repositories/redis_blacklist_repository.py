import logging

from redis.asyncio.client import Pipeline

from core.exceptions import RedisConnectionException
from ports.repositories.blacklist_repository import BlacklistRepository

logger = logging.getLogger(__name__)


class RedisBlacklistRepository(BlacklistRepository):
    def __init__(self, session: Pipeline):
        self.session = session

    async def add(self, token: str, token_exp: int):
        try:
            await self.session.set("bl_" + token, token)
            await self.session.expireat("bl_" + token, token_exp)
            await self.session.execute()
        except Exception as e:
            logger.exception(e)
            raise RedisConnectionException

    async def check(self, token: str) -> bool:
        try:
            await self.session.get("bl_" + token)
            token_res = await self.session.execute()

            if not token_res[0]:
                return False
            return True
        except Exception as e:
            logger.exception(e)
            raise RedisConnectionException
