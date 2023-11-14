import pytest

from adapters.auth.auth_jwt import JwtAuth
from adapters.auth.passlib_hashing import PasslibHashing
from adapters.repositories.in_memory_user_repository import InMemoryUserRepository
from core.settings import Settings
from domain.group import Group
from domain.user import RoleEnum, User
from usecase.auth_usecase import LoginUseCase, SignupUseCase


@pytest.fixture()
def settings(monkeypatch):
    monkeypatch.setenv("JWT_SECRET", "cf6b56353597d5a0cd253b57b5cea25fd689f433ce3b40f5")
    monkeypatch.setenv("DB_NAME", "UserManagment")
    monkeypatch.setenv("DB_USER", "root")
    monkeypatch.setenv("DB_PASSWORD", "abfkrf2003")
    monkeypatch.setenv("DB_HOST", "localhost")
    monkeypatch.setenv("DB_PORT", "5432")

    return Settings()


@pytest.fixture()
def auth_repository(settings):
    return JwtAuth(settings)


@pytest.fixture
def user_repository():
    return InMemoryUserRepository()


@pytest.fixture()
def password_hashing():
    return PasslibHashing()


@pytest.fixture()
def signup_use_case(auth_repository, user_repository, password_hashing):
    return SignupUseCase(auth_repository, user_repository, password_hashing)


@pytest.fixture()
def login_use_case(auth_repository, user_repository, password_hashing):
    return LoginUseCase(auth_repository, user_repository, password_hashing)


@pytest.mark.asyncio
async def test_signup_use_case(signup_use_case, user_repository):
    user_id = await signup_use_case(
        user=User(
            name="test1",
            surname="test1",
            username="test1",
            phone_number="+375 44 562-24-75",
            email="test1@gtest1.com",
            group=Group(id=1),
            role=RoleEnum.user,
            password="1234567",
        )
    )

    assert user_id is not None
    assert user_repository.get_user(user_id) is not None


@pytest.mark.asyncio
async def test_login_use_case(signup_use_case, login_use_case, user_repository):
    user_id = await signup_use_case(
        user=User(
            name="test1",
            surname="test1",
            username="test1",
            phone_number="+375 44 562-24-75",
            email="test1@gtest1.com",
            group=Group(id=1),
            role=RoleEnum.user,
            password="1234567",
        )
    )

    assert user_repository.get_user(user_id) is not None

    token = await login_use_case({"username": "test1", "password": "1234567"})
    assert token is not None
