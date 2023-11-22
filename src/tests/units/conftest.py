import uuid

import pytest

from adapters.auth.auth_jwt import JwtAuth
from adapters.auth.in_memory_auth import InMemoryAuth
from adapters.auth.passlib_hashing import PasslibHashing
from adapters.repositories.in_memory_redis_repository import (
    InMemoryRedisBlacklistRepository,
)
from adapters.repositories.in_memory_user_repository import InMemoryUserRepository
from core.settings import Settings
from domain.group import Group
from domain.user import RoleEnum, User
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


@pytest.fixture()
def settings(monkeypatch):
    monkeypatch.setenv("JWT_SECRET", "cf6b56353597d5a0cd253b57b5cea25fd689f433ce3b40f5")
    monkeypatch.setenv("DB_NAME", "UserManagment")
    monkeypatch.setenv("DB_USER", "root")
    monkeypatch.setenv("DB_PASSWORD", "abfkrf2003")
    monkeypatch.setenv("DB_HOST", "localhost")
    monkeypatch.setenv("DB_PORT", "5432")
    monkeypatch.setenv(
        "BUCKET_NAME", "user-management-b4714add-d7b8-40dd-9158-21bd006d686f"
    )
    monkeypatch.setenv("AWS_ACCESS_KEY_ID", "test")
    monkeypatch.setenv("AWS_SECRET_ACCESS_KEY", "test")
    monkeypatch.setenv("REDIS_HOST", "localhost")
    monkeypatch.setenv("REDIS_PORT", "6379")

    return Settings()


@pytest.fixture()
def user_test():
    return User(
        name="test1",
        surname="test1",
        username="test1",
        phone_number="+375 44 562-24-75",
        email="test1@gtest1.com",
        group=Group(id=uuid.uuid4()),
        role=RoleEnum.user,
        password="1234567",
    )


@pytest.fixture()
def users_list():
    group_id = uuid.uuid4()
    return [
        User(
            name="test1",
            surname="test1",
            username="test1",
            phone_number="+375 44 111-11-11",
            email="test1@gtest.com",
            group=Group(id=group_id),
            role=RoleEnum.user,
            password="1234567",
        ),
        User(
            name="test2",
            surname="test2",
            username="test2",
            phone_number="+375 44 222-22-22",
            email="test2@gtest.com",
            group=Group(id=group_id),
            role=RoleEnum.moderator,
            password="1234567",
        ),
        User(
            name="test3",
            surname="test3",
            username="test3",
            phone_number="+375 44 333-33-33",
            email="test3@gtest.com",
            group=Group(id=group_id),
            role=RoleEnum.admin,
            password="1234567",
        ),
        User(
            name="test4",
            surname="test4",
            username="test4",
            phone_number="+375 44 444-44-44",
            email="test4@gtest.com",
            group=Group(id=uuid.uuid4()),
            role=RoleEnum.user,
            password="1234567",
        ),
    ]


@pytest.fixture()
def auth_service(settings):
    return JwtAuth(settings)


@pytest.fixture()
def in_memory_auth_service():
    return InMemoryAuth()


@pytest.fixture
def user_repository():
    return InMemoryUserRepository()


@pytest.fixture()
def password_hashing():
    return PasslibHashing()


@pytest.fixture()
def blacklist_repository():
    return InMemoryRedisBlacklistRepository()


@pytest.fixture()
def get_current_user_use_case(
    in_memory_auth_service, user_repository, blacklist_repository
):
    return GetCurrentUserUseCase(
        in_memory_auth_service, user_repository, blacklist_repository
    )


@pytest.fixture()
def refresh_token_use_case(in_memory_auth_service, blacklist_repository):
    return RefreshTokenUseCase(in_memory_auth_service, blacklist_repository)


@pytest.fixture()
def signup_use_case(user_repository, password_hashing):
    return SignupUseCase(user_repository, password_hashing)


@pytest.fixture()
def login_use_case(in_memory_auth_service, user_repository, password_hashing):
    return LoginUseCase(in_memory_auth_service, user_repository, password_hashing)


@pytest.fixture()
def get_users_use_case(user_repository):
    return GetUsersUseCase(user_repository)


@pytest.fixture()
def get_user_use_case(user_repository):
    return GetUserUseCase(user_repository)


@pytest.fixture()
def delete_user_use_case(user_repository):
    return DeleteUserUseCase(user_repository)


@pytest.fixture()
def update_user_use_case(user_repository):
    return UpdateUserUseCase(user_repository)
