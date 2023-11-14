from abc import ABC, abstractmethod

from domain.user import User


class UserRepository(ABC):
    @abstractmethod
    async def save_user(self, user: User) -> int:
        pass

    @abstractmethod
    async def get_users(self, **kwargs) -> list[User]:
        pass

    @abstractmethod
    async def get_user(self, user_id: int) -> User:
        pass

    @abstractmethod
    async def get_user_by_username(self, username: str) -> User:
        pass

    @abstractmethod
    async def get_user_by_email(self, email: str) -> User:
        pass

    @abstractmethod
    async def get_user_by_phone_number(self, phone_number: str) -> User:
        pass

    @abstractmethod
    async def update_user(self, user_id: int, user_data: dict) -> User:
        pass

    @abstractmethod
    async def delete_user(self, user_id: int):
        pass
