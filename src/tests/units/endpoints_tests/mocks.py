import uuid
from typing import Annotated, Any

from fastapi import Depends

from dependencies.dependencies import oauth2_scheme
from domain.group import Group
from domain.user import RoleEnum, User


def mock_signup():
    return MockSignupUseCase()


def mock_login():
    return MockLoginUseCase()


def mock_refresh():
    return MockRefreshUseCase()


def mock_reset():
    return MockResetPasswordUseCase()


def mock_get_users():
    return MockGetUsersUseCase()


async def mock_get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    return await MockGetCurrentUserUseCase()()


def mock_update_user():
    return MockUpdateUserUseCase()


def mock_delete_user():
    return MockDeleteUserUseCase()


def mock_get_user():
    return MockGetUserUseCase()


class MockSignupUseCase:
    async def __call__(self, user):
        return uuid.uuid4()


class MockLoginUseCase:
    async def __call__(self, user_data: dict[str, Any]):
        return {"access_token": uuid.uuid4(), "token_type": "bearer"}


class MockRefreshUseCase:
    async def __call__(self, old_token: str):
        return {"access_token": uuid.uuid4(), "token_type": "bearer"}


class MockResetPasswordUseCase:
    async def __call__(self, email: str):
        pass


class MockGetCurrentUserUseCase:
    async def __call__(self):
        return User(
            id=uuid.uuid4(),
            name="test1",
            surname="test1",
            username="test1",
            phone_number="+375 44 111-11-11",
            email="test1@test.com",
            role=RoleEnum.admin,
            group=Group(id=uuid.uuid4(), name="group1"),
            password="1234567",
        )


class MockUpdateUserUseCase:
    async def __call__(self, current_user: User, user_id: uuid.UUID, user_data: User):
        return user_id


class MockDeleteUserUseCase:
    async def __call__(self, user_id: uuid.UUID):
        return 1


class MockGetUserUseCase:
    async def __call__(self, user_id: uuid.UUID, group_id: uuid.UUID, role: RoleEnum):
        return User(
            id=user_id,
            name="test1",
            surname="test1",
            username="test1",
            phone_number="+375 44 111-11-11",
            email="test1@test.com",
            role=RoleEnum.admin,
            group=Group(id=group_id, name="group1"),
            password="1234567",
        )


class MockGetUsersUseCase:
    async def __call__(self, group_id: uuid.UUID, role: RoleEnum, **kwargs):
        return [
            User(
                id=uuid.uuid4(),
                name="test1",
                surname="test1",
                username="test1",
                phone_number="+375 44 111-11-11",
                email="test1@test.com",
                role=RoleEnum.admin,
                group=Group(id=uuid.uuid4(), name="group1"),
                password="1234567",
            )
        ]
