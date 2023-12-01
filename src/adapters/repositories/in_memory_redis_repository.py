from ports.repositories.blacklist_repository import BlacklistRepository


class InMemoryRedisBlacklistRepository(BlacklistRepository):
    def __init__(self):
        self.blacklist = {}

    async def add(self, token: str, token_exp: int):
        self.blacklist[token] = token

    async def check(self, token: str) -> bool:
        if self.blacklist.get(token) is None:
            return False

        return True
