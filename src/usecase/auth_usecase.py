import uuid
from typing import Any

from core.exceptions import (
    AuthenticationException,
    AuthorizationException,
    TokenDenied,
    UserIsBlockedException,
    UserNotFoundException,
)
from domain.user import User
from ports.repositories.auth_service import AuthService
from ports.repositories.blacklist_repository import BlacklistRepository
from ports.repositories.notification_service import NotificationService
from ports.repositories.password_hashing import PasswordHashing
from ports.repositories.user_repository import UserRepository


class LoginUseCase:
    def __init__(
        self,
        auth_repository: AuthService,
        user_repository: UserRepository,
        password_hashing: PasswordHashing,
    ):
        self.auth_repository = auth_repository
        self.user_repository = user_repository
        self.password_hashing = password_hashing

    async def __call__(self, user_data: dict[str, Any]) -> dict[str, str]:
        user = await self.user_repository.get_user_by_filter(user_data.get("user_data"))
        if not user:
            raise UserNotFoundException

        if not self.password_hashing.verify_password(
            user_data.get("password"), user.password
        ):
            raise AuthenticationException

        token = self.auth_repository.create_token(
            user_id=user.id, group_id=user.group.id, role=user.role
        )
        refresh_token = self.auth_repository.create_refresh_token(user_id=user.id)
        return {
            "access_token": token,
            "refresh_token": refresh_token,
            "token_type": "bearer",
        }


class GetCurrentUserUseCase:
    def __init__(
        self,
        auth_repository: AuthService,
        user_repository: UserRepository,
        blacklist: BlacklistRepository,
    ):
        self.auth_repository = auth_repository
        self.user_repository = user_repository
        self.blacklist = blacklist

    async def __call__(self, token):
        # if await self.blacklist.check(token) is True:
        #     raise TokenDenied
        info = self.auth_repository.parse_token(token)
        if not info.get("token_type"):
            raise TokenDenied

        if info.get("token_type") != "access":
            raise TokenDenied

        user_id: uuid.UUID = info.get("user_id")

        if user_id is None:
            raise AuthorizationException

        user = await self.user_repository.get_user(user_id)

        if not user:
            raise UserNotFoundException

        if user.is_blocked:
            raise UserIsBlockedException

        return user


class SignupUseCase:
    def __init__(
        self,
        user_repository: UserRepository,
        password_hashing: PasswordHashing,
    ):
        self.user_repository = user_repository
        self.password_hashing = password_hashing

    async def __call__(self, user: User) -> uuid.UUID:
        user.password = self.password_hashing.hash_password(user.password)
        user_id = await self.user_repository.save_user(user)

        return user_id


class RefreshTokenUseCase:
    def __init__(
        self,
        auth_repository: AuthService,
        blacklist: BlacklistRepository,
        user_repository: UserRepository,
    ):
        self.auth_repository = auth_repository
        self.blacklist = blacklist
        self.user_repository = user_repository

    async def __call__(self, old_token: str):
        info = self.auth_repository.parse_token(old_token)

        if not info.get("token_type"):
            raise TokenDenied

        if info.get("token_type") != "refresh":
            raise TokenDenied

        if not info.get("user_id"):
            raise TokenDenied

        await self.blacklist.add(old_token, info.get("exp"))

        user = await self.user_repository.get_user(info.get("user_id"))

        if not user:
            raise UserNotFoundException

        token = self.auth_repository.create_token(
            user_id=user.id, group_id=user.group.id, role=user.role
        )
        refresh_token = self.auth_repository.create_refresh_token(
            user_id=info.get("user_id")
        )
        return {
            "access_token": token,
            "refresh_token": refresh_token,
            "token_type": "bearer",
        }


class ResetPasswordUseCase:
    def __init__(
        self, user_repository: UserRepository, notification_service: NotificationService
    ):
        self.user_repository = user_repository
        self.notification_service = notification_service

    async def __call__(self, email: str):
        user = await self.user_repository.get_user_by_filter(email)
        if not user:
            raise UserNotFoundException

        self.notification_service.publish_message(
            email, "There is example email!", "UserManagement. Reset-password"
        )
