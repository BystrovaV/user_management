from typing import Any

from core.exceptions import (
    AuthenticationException,
    AuthorizationException,
    TokenDenied,
    UserNotFoundException,
)
from domain.user import User
from ports.repositories.auth_repository import AuthRepository
from ports.repositories.blacklist_repository import BlacklistRepository
from ports.repositories.password_hashing import PasswordHashing
from ports.repositories.user_repository import UserRepository


class LoginUseCase:
    def __init__(
        self,
        auth_repository: AuthRepository,
        user_repository: UserRepository,
        password_hashing: PasswordHashing,
    ):
        self.auth_repository = auth_repository
        self.user_repository = user_repository
        self.password_hashing = password_hashing

    # username: str, password: str
    async def __call__(self, user_data: dict[str, Any]) -> dict[str, str]:
        # print(user_data)
        if user_data.get("username"):
            user = await self.user_repository.get_user_by_username(
                user_data.get("username")
            )
        elif user_data.get("email"):
            user = await self.user_repository.get_user_by_email(user_data.get("email"))
        elif user_data.get("phone_number"):
            user = await self.user_repository.get_user_by_phone_number(
                user_data.get("phone_number")
            )
        else:
            raise Exception("Invalid input")

        if not user:
            raise UserNotFoundException

        if not self.password_hashing.verify_password(
            user_data.get("password"), user.password
        ):
            raise AuthenticationException

        token = self.auth_repository.create_token(user_id=user.id)
        return {"access_token": token, "token_type": "bearer"}


class GetCurrentUserUseCase:
    def __init__(
        self,
        auth_repository: AuthRepository,
        user_repository: UserRepository,
        blacklist: BlacklistRepository,
    ):
        self.auth_repository = auth_repository
        self.user_repository = user_repository
        self.blacklist = blacklist

    async def __call__(self, token):
        if await self.blacklist.check(token) is True:
            raise AuthorizationException

        user_id: int = self.auth_repository.parse_token(token).get("user_id")

        if user_id is None:
            raise AuthorizationException

        user = await self.user_repository.get_user(user_id)

        if not user:
            raise UserNotFoundException

        return user


class SignupUseCase:
    def __init__(
        self,
        auth_repository: AuthRepository,
        user_repository: UserRepository,
        password_hashing: PasswordHashing,
    ):
        self.auth_repository = auth_repository
        self.user_repository = user_repository
        self.password_hashing = password_hashing

    async def __call__(self, user: User) -> int:
        user.password = self.password_hashing.hash_password(user.password)
        user_id = await self.user_repository.save_user(user)

        return user_id


class RefreshTokenUseCase:
    def __init__(self, auth_repository: AuthRepository, blacklist: BlacklistRepository):
        self.auth_repository = auth_repository
        self.blacklist = blacklist

    async def __call__(self, old_token: str):
        info = self.auth_repository.parse_token(old_token)

        if not info.get("user_id"):
            raise TokenDenied

        await self.blacklist.add(old_token, info.get("exp"))

        token = self.auth_repository.create_token(user_id=info.get("user_id"))
        return {"access_token": token, "token_type": "bearer"}
