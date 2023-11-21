from abc import ABC, abstractmethod


class BlacklistRepository(ABC):
    @abstractmethod
    async def add(self, token: str, token_exp: int):
        pass

    @abstractmethod
    async def check(self, token: str):
        pass
