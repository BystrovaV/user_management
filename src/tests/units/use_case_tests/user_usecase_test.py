import pytest

from core.exceptions import AccessDenied
from domain.user import RoleEnum


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


@pytest.mark.asyncio
async def test_delete_user_use_case(
    delete_user_use_case, signup_use_case, user_repository, users_list
):
    for user in users_list:
        await signup_use_case(user)
    assert len(user_repository.users) == len(users_list)

    rowcount = await delete_user_use_case(users_list[0].id)
    assert rowcount == 1
    assert len(user_repository.users) == len(users_list) - 1


@pytest.mark.asyncio
async def test_update_user_use_case(
    update_user_use_case, signup_use_case, user_repository, users_list
):
    user = users_list[0]
    await signup_use_case(user)
    assert len(user_repository.users) == 1

    user.username = "update"
    user_id = await update_user_use_case(user, user.id, user)
    assert user.id == user_id
    assert user.username == "update"
