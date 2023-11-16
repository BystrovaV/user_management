import uuid
from abc import ABC, abstractmethod


class AuthService(ABC):
    @abstractmethod
    def create_token(self, user_id: uuid.UUID) -> str:
        pass

    @abstractmethod
    def parse_token(self, token) -> dict:
        pass
