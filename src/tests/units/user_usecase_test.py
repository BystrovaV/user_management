import pytest

from adapters.repositories.in_memory_user_repository import InMemoryUserRepository
from core.exceptions import AccessDenied
from domain.group import Group
from domain.user import RoleEnum, User
from usecase.user_usecase import GetUsersUseCase, GetUserUseCase


@pytest.fixture()
def get_users_use_case(user_repository):
    return GetUsersUseCase(user_repository)


@pytest.fixture()
def get_user_use_case(user_repository):
    return GetUserUseCase(user_repository)


@pytest.mark.asyncio
async def test_get_users(
    signup_use_case, get_users_use_case, user_repository, users_list
):
    for user in users_list:
        await signup_use_case(user)

    assert len(user_repository.users) == len(users_list)

    admin = None
    user = None
    moderator = None
    for item in users_list:
        if item.role == RoleEnum.admin:
            admin = item
        elif item.role == RoleEnum.moderator:
            moderator = item
        elif item.role == RoleEnum.user:
            user = item

    users = await get_users_use_case(group_id=admin.group, role=admin.role, **{})
    assert len(users) == len(user_repository.users)

    users = await get_users_use_case(
        group_id=moderator.group, role=moderator.role, **{}
    )
    for user in users:
        assert user.group.id == moderator.group.id

    with pytest.raises(AccessDenied):
        await get_users_use_case(group_id=user.group.id, role=user.role, **{})


@pytest.mark.asyncio
async def test_get_user_use_case(
    signup_use_case, get_user_use_case, user_repository, users_list
):
    for user in users_list:
        await signup_use_case(user)

    assert len(user_repository.users) == len(users_list)

    admin = None
    user = None
    moderator = None
    for item in users_list:
        if item.role == RoleEnum.admin:
            admin = item
        elif item.role == RoleEnum.moderator:
            moderator = item
        elif item.role == RoleEnum.user:
            user = item

    with pytest.raises(AccessDenied):
        await get_user_use_case(user_id=user.id, group_id=user.group.id, role=user.role)

    user = await get_user_use_case(
        user_id=user.id, group_id=admin.group.id, role=admin.role
    )
    assert user is not None
