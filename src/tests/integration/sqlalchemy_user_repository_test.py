import pytest
import pytest_asyncio
from sqlalchemy import delete

from adapters.orm_engines.models import GroupORM, UserORM
from adapters.repositories.sqlalchemy_user_repository import SqlAlchemyUserRepository
from core.exceptions import UserNotFoundException
from domain.group import Group
from domain.user import RoleEnum, User


@pytest_asyncio.fixture
async def user_repository(session):
    repository = SqlAlchemyUserRepository(session)
    yield repository
    await repository.session.execute(delete(UserORM))
    await repository.session.execute(delete(GroupORM))


@pytest.mark.asyncio
async def test_user_save_to_db(user_repository, session):
    group = GroupORM(name="group1")
    session.add(group)

    await session.commit()
    await session.refresh(group)

    user = User(
        name="test1",
        surname="test1",
        username="test1",
        phone_number="+375 44 111-11-11",
        email="test1@gtest.com",
        group=Group(id=group.id),
        role=RoleEnum.user,
        password="1234567",
    )

    user.id = await user_repository.save_user(user)
    assert user.id is not None

    user.username = "test1_update"
    user_id_new = await user_repository.save_user(user)
    assert user_id_new == user.id


@pytest.mark.asyncio
async def test_get_user(user_repository, session):
    group = GroupORM(name="group1")
    session.add(group)

    await session.commit()
    await session.refresh(group)

    user = User(
        name="test1",
        surname="test1",
        username="test1",
        phone_number="+375 44 111-11-11",
        email="test1@gtest.com",
        group=Group(id=group.id),
        role=RoleEnum.user,
        password="1234567",
    )

    user.id = await user_repository.save_user(user)

    user_db = await user_repository.get_user(user.id)
    assert user.id == user_db.id
    assert (
        user.name == user_db.name
        and user.username == user_db.username
        and user.email == user_db.email
        and user.phone_number == user_db.phone_number
    )


@pytest.mark.asyncio
async def test_get_user_by_filter(user_repository, session):
    group = GroupORM(name="group1")
    session.add(group)

    await session.commit()
    await session.refresh(group)

    user = User(
        name="test1",
        surname="test1",
        username="test1",
        phone_number="+375 44 111-11-11",
        email="test1@gtest.com",
        group=Group(id=group.id),
        role=RoleEnum.user,
        password="1234567",
    )

    user.id = await user_repository.save_user(user)

    user_db = await user_repository.get_user_by_filter(user.username)
    assert user.id == user_db.id
    assert (
        user.name == user_db.name
        and user.username == user_db.username
        and user.email == user_db.email
        and user.phone_number == user_db.phone_number
    )

    user_db = await user_repository.get_user_by_filter(user.email)
    assert user.id == user_db.id
    assert (
        user.name == user_db.name
        and user.username == user_db.username
        and user.email == user_db.email
        and user.phone_number == user_db.phone_number
    )


@pytest.mark.asyncio
async def test_delete_user(user_repository, session):
    group = GroupORM(name="group1")
    session.add(group)

    await session.commit()
    await session.refresh(group)

    user = User(
        name="test1",
        surname="test1",
        username="test1",
        phone_number="+375 44 111-11-11",
        email="test1@gtest.com",
        group=Group(id=group.id),
        role=RoleEnum.user,
        password="1234567",
    )

    user.id = await user_repository.save_user(user)
    await user_repository.delete_user(user.id)

    with pytest.raises(UserNotFoundException):
        await user_repository.get_user(user.id)


@pytest.mark.asyncio
async def test_add_image(user_repository, session):
    group = GroupORM(name="group1")
    session.add(group)

    await session.commit()
    await session.refresh(group)

    user = User(
        name="test1",
        surname="test1",
        username="test1",
        phone_number="+375 44 111-11-11",
        email="test1@gtest.com",
        group=Group(id=group.id),
        role=RoleEnum.user,
        password="1234567",
    )

    user.id = await user_repository.save_user(user)
    await user_repository.add_image(user.id, "image")

    assert (await user_repository.get_user(user.id)).image_path == "image"
