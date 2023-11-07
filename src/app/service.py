from sqlalchemy import delete, desc, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import *
from app.schemas import UserBase, UsersQueryParams


async def get_users(session: AsyncSession, params: UsersQueryParams) -> list[User]:
    stmt = select(User)

    if params.filter_by_name:
        stmt = stmt.filter_by(name=params.filter_by_name)

    if params.sort_by and params.order_by == "desc":
        stmt = stmt.order_by(desc(params.sort_by.value))
    elif params.sort_by:
        stmt = stmt.order_by(params.sort_by.value)

    if params.limit and params.page:
        stmt = stmt.limit(params.limit).offset((params.page - 1) * params.limit)
    # Как организовывать постранично?

    result = await session.execute(stmt)

    return result.scalars().all()


async def get_user(
    session: AsyncSession, user_id: int, group_id: int | None = None
) -> User:
    stmt = select(User).where(User.id == user_id)
    if group_id:
        stmt = stmt.where(User.group == group_id)

    result = await session.execute(stmt)

    return result.scalar()


async def get_user_by_username(session: AsyncSession, username: str) -> User:
    result = await session.execute(select(User).where(User.username == username))

    return result.scalar()


def insert_user(session: AsyncSession, user: UserBase):
    new_user = User(
        name=user.name,
        surname=user.surname,
        username=user.username,
        phone_number=user.phone_number,
        email=user.email,
        role=user.role,
        group=user.group,
    )
    session.add(new_user)
    return new_user


async def delete_user(session: AsyncSession, user_id: int):
    stmt = delete(User).where(User.id == user_id)
    result = await session.execute(stmt)

    if result.rowcount:
        await session.commit()

    return result.rowcount


async def get_groups(session: AsyncSession) -> list[Group]:
    result = await session.execute(select(Group))

    return result.scalars().all()


async def get_group(session: AsyncSession, group_id: int) -> Group:
    result = await session.execute(select(Group).where(Group.id == group_id))

    return result.scalar()


def insert_group(session: AsyncSession, group_name: str):
    group = Group(name=group_name)
    session.add(group)

    return group
