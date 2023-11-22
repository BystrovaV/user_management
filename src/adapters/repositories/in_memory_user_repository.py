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
        users = self.users
        if kwargs.get("filter_by_name"):
            users = list(
                filter(lambda x: x.name == kwargs.get("filter_by_name"), users)
            )

        if kwargs.get("group_id"):
            users = list(filter(lambda x: x.group.id == kwargs.get("group_id"), users))

        return users

    async def get_user(self, user_id: uuid.UUID) -> User:
        for user in self.users:
            if user.id == user_id:
                return user

    async def get_user_by_filter(self, filter: str) -> User:
        for user in self.users:
            if user.username == filter or user.phone_number == filter or user.email:
                return user

    async def delete_user(self, user_id: uuid.UUID):
        user = await self.get_user(user_id)
        self.users.remove(user)
        return 1

    async def add_image(self, user_id: uuid.UUID, image_path: str) -> str:
        pass
