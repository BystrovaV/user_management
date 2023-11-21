import uuid

from domain.user import User
from ports.repositories.user_repository import UserRepository


class InMemoryUserRepository(UserRepository):
    def __init__(self):
        self.users = []

    async def save_user(self, user: User) -> uuid.UUID:
        user.id = uuid.uuid4()
        self.users.append(user)
        return user.id

    async def get_users(self, **kwargs) -> list[User]:
        return self.users

    async def get_user(self, user_id: uuid.UUID) -> User:
        for user in self.users:
            if user.id == user_id:
                return user

    async def get_user_by_filter(self, filter: str) -> User:
        pass

    # async def get_user_by_username(self, username: str) -> User:
    #     for user in self.users:
    #         if user.username == username:
    #             return user
    #
    # async def get_user_by_email(self, email: str) -> User:
    #     for user in self.users:
    #         if user.email == email:
    #             return user
    #
    # async def get_user_by_phone_number(self, phone_number: str) -> User:
    #     for user in self.users:
    #         if user.phone_number == phone_number:
    #             return user

    async def delete_user(self, user_id: uuid.UUID):
        pass

    # async def update_user(self, user_id: int, user_data: dict) -> User:
    #     for user in self.users:
    #         if user.id == user_id:
    #             if user_data.get("name"):
    #                 user.name = user_data.get("name")
    #
    #             if user_data.get("surname"):
    #                 user.surname = user_data.get("surname")
    #
    #             if user_data.get("username"):
    #                 user.username = user_data.get("username")
    #
    #             if user_data.get("email"):
    #                 user.email = user_data.get("email")
    #
    #             if user_data.get("phone_number"):
    #                 user.phone_number = user_data.get("phone_number")
    #             return user
