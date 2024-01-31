import uuid
from abc import ABC, abstractmethod

from domain.user import RoleEnum


class AuthService(ABC):
    @abstractmethod
    def create_token(
        self, user_id: uuid.UUID, group_id: uuid.UUID, role: RoleEnum
    ) -> str:
        pass

    @abstractmethod
    def parse_token(self, token) -> dict:
        pass

    @abstractmethod
    def create_refresh_token(self, user_id: uuid.UUID) -> str:
        pass
