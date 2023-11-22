from typing import Annotated

from fastapi import Depends, UploadFile
from fastapi.security import OAuth2PasswordBearer

from adapters.auth.auth_jwt import JwtAuth
from adapters.auth.passlib_hashing import PasslibHashing
from adapters.localstack.localstack import LocalStackS3Repository, LocalStackSESService
from adapters.repositories.redis_blacklist_repository import RedisBlacklistRepository
from adapters.repositories.sqlalchemy_user_repository import SqlAlchemyUserRepository
from core.exceptions import InvalidImageException
from core.settings import get_settings
from dependencies.database import get_session
from dependencies.localstack_dependency import (
    get_localstack_s3_client,
    get_localstack_ses_client,
)
from dependencies.redis_dependency import get_redis_connection
from usecase.auth_usecase import (
    GetCurrentUserUseCase,
    LoginUseCase,
    RefreshTokenUseCase,
    ResetPasswordUseCase,
    SignupUseCase,
)
from usecase.user_usecase import (
    DeleteUserUseCase,
    GetUsersUseCase,
    GetUserUseCase,
    UpdateUserUseCase,
    UploadImageUseCase,
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


def get_user_repository(session=Depends(get_session)):
    return SqlAlchemyUserRepository(session)


def get_redis_blacklist_repository(redis=Depends(get_redis_connection)):
    return RedisBlacklistRepository(redis)


def get_localstack_s3_repository(
    localstack=Depends(get_localstack_s3_client), settings=Depends(get_settings)
):
    return LocalStackS3Repository(localstack, settings)


def get_upload_image_use_case(
    localstack_repository=Depends(get_localstack_s3_repository),
    user_repository=Depends(get_user_repository),
):
    return UploadImageUseCase(
        image_repository=localstack_repository, user_repository=user_repository
    )


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
    user_repository=Depends(get_user_repository),
    password_hashing=Depends(get_passlib_hashing),
):
    return SignupUseCase(user_repository, password_hashing)


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


def check_file_format(image: UploadFile):
    if image.content_type.startswith("image/"):
        return image
    raise InvalidImageException


def get_localstack_ses_service(client=Depends(get_localstack_ses_client)):
    return LocalStackSESService(client)


def get_reset_password_use_case(service=Depends(get_localstack_ses_service)):
    return ResetPasswordUseCase(service)
