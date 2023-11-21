from typing import Annotated

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer

from adapters.auth.auth_jwt import JwtAuth
from adapters.auth.passlib_hashing import PasslibHashing
from adapters.repositories.redis_blacklist_repository import RedisBlacklistRepository
from adapters.repositories.sqlalchemy_user_repository import SqlAlchemyUserRepository
from core.settings import Settings
from dependencies.database import get_session
from dependencies.redis_dependency import get_redis_connection
from usecase.auth_usecase import (
    GetCurrentUserUseCase,
    LoginUseCase,
    RefreshTokenUseCase,
    SignupUseCase,
)
from usecase.user_usecase import (
    DeleteUserUseCase,
    GetUsersUseCase,
    GetUserUseCase,
    UpdateUserUseCase,
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


def get_settings():
    return Settings()


def get_user_repository(session=Depends(get_session)):
    return SqlAlchemyUserRepository(session)


def get_redis_blacklist_repository(redis=Depends(get_redis_connection)):
    return RedisBlacklistRepository(redis)


# def get_save_user_use_case(repository=Depends(get_user_repository)):
#     return SaveUserUseCase(repository)


def get_users_use_case(repository=Depends(get_user_repository)):
    return GetUsersUseCase(repository)


def get_auth_repository(settings=Depends(get_settings)):
    return JwtAuth(settings)


def get_passlib_hashing():
    return PasslibHashing()


def get_login_use_case(
    auth_repository=Depends(get_auth_repository),
    user_repository=Depends(get_user_repository),
    password_hashing=Depends(get_passlib_hashing),
):
    return LoginUseCase(auth_repository, user_repository, password_hashing)


def get_signup_use_case(
    auth_repository=Depends(get_auth_repository),
    user_repository=Depends(get_user_repository),
    password_hashing=Depends(get_passlib_hashing),
):
    return SignupUseCase(auth_repository, user_repository, password_hashing)


def get_refresh_token_use_case(
    auth_repository=Depends(get_auth_repository),
    blacklist=Depends(get_redis_blacklist_repository),
):
    return RefreshTokenUseCase(auth_repository, blacklist)


async def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)],
    auth_repository=Depends(get_auth_repository),
    user_repository=Depends(get_user_repository),
    blacklist=Depends(get_redis_blacklist_repository),
):
    return await GetCurrentUserUseCase(auth_repository, user_repository, blacklist)(
        token
    )


def get_user_use_case(user_repository=Depends(get_user_repository)):
    return GetUserUseCase(user_repository)


def update_user_use_case(user_repository=Depends(get_user_repository)):
    return UpdateUserUseCase(user_repository)


def delete_user_use_case(user_repository=Depends(get_user_repository)):
    return DeleteUserUseCase(user_repository)
