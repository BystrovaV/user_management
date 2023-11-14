from abc import ABC, abstractmethod


class AuthRepository(ABC):
    @abstractmethod
    def create_token(self, user_id: int) -> str:
        pass

    @abstractmethod
    def parse_token(self, token) -> dict:
        pass
