import uuid
from abc import ABC, abstractmethod

from domain.user import User


class UserRepository(ABC):
    @abstractmethod
    async def save_user(self, user: User) -> uuid.UUID:
        pass

    @abstractmethod
    async def get_users(self, **kwargs) -> list[User]:
        pass

    @abstractmethod
    async def get_user(self, user_id: uuid.UUID) -> User:
        pass

    @abstractmethod
    async def get_user_by_filter(self, filter: str) -> User:
        pass

    # @abstractmethod
    # async def update_user(self, user_id: int, user_data: dict) -> User:
    #     pass

    @abstractmethod
    async def delete_user(self, user_id: uuid.UUID):
        pass

    @abstractmethod
    async def add_image(self, user_id: uuid.UUID, image_path: str) -> str:
        pass
