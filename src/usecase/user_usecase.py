from core.exceptions import AccessDenied
from domain.user import RoleEnum, User
from ports.repositories.user_repository import UserRepository


class GetUsersUseCase:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    async def __call__(self, group_id: int, role: RoleEnum, **kwargs) -> list[User]:
        if role == RoleEnum.user:
            raise AccessDenied
        elif role == RoleEnum.moderator:
            return await self.user_repository.get_users(
                **dict(kwargs, group_id=group_id)
            )

        return await self.user_repository.get_users(**kwargs)


class GetUserUseCase:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    async def __call__(self, user_id: int, group_id: int, role: RoleEnum) -> User:
        user = await self.user_repository.get_user(user_id)

        if role == RoleEnum.user:
            raise AccessDenied
        elif role == RoleEnum.moderator and user.group != group_id:
            raise AccessDenied

        return user


class DeleteUserUseCase:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    async def __call__(self, user_id: int):
        rowcount = await self.user_repository.delete_user(user_id)
        return rowcount


class UpdateUserUseCase:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    async def __call__(
        self, current_user: User, updated_user_id: int, user_data: dict
    ) -> User:
        if current_user.role != RoleEnum.admin and current_user.id != updated_user_id:
            raise AccessDenied

        return await self.user_repository.update_user(updated_user_id, user_data)
        # pass
