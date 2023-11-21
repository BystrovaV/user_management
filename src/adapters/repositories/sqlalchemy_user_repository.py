import uuid

from sqlalchemy import delete, desc, or_, select
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from adapters.orm_engines.models import UserORM
from core.exceptions import (
    DatabaseConnectionException,
    UserAlreadyExistsException,
    UserNotFoundException,
)
from domain.user import User
from ports.repositories.user_repository import UserRepository


class SqlAlchemyUserRepository(UserRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def save_user(self, user: User) -> uuid.UUID:
        try:
            stmt = select(UserORM).where(UserORM.id == user.id)
            result = await self.session.execute(stmt)

            new_user = result.scalars().first()
            if new_user is None:
                new_user = UserORM()
                self.session.add(new_user)
                new_user.role = user.role
                new_user.group = user.group.id
                new_user.password = user.password

            new_user.name = user.name
            new_user.surname = user.surname
            new_user.username = user.username
            new_user.phone_number = user.phone_number
            new_user.email = user.email
            new_user.is_blocked = user.is_blocked

            await self.session.flush()
            return new_user.id
        except IntegrityError as e:
            await self.session.rollback()
            raise UserAlreadyExistsException
        except SQLAlchemyError as e:
            await self.session.rollback()
            raise DatabaseConnectionException(e)

    async def get_users(self, **kwargs) -> list[User]:
        try:
            stmt = select(UserORM)

            if kwargs.get("filter_by_name"):
                stmt = stmt.filter_by(name=kwargs.get("filter_by_name"))

            if kwargs.get("group_id"):
                stmt = stmt.filter_by(group=kwargs.get("group_id"))

            if kwargs.get("sort_by") and kwargs.get("order_by") == "desc":
                stmt = stmt.order_by(desc(kwargs.get("sort_by")))
            elif kwargs.get("sort_by"):
                stmt = stmt.order_by(kwargs.get("sort_by"))

            if kwargs.get("limit") and kwargs.get("page"):
                stmt = stmt.limit(kwargs.get("limit")).offset(
                    (kwargs.get("page") - 1) * kwargs.get("limit")
                )

            result = await self.session.execute(stmt)

            domain_result = []
            for res in result.scalars().all():
                domain_result.append(
                    SqlAlchemyUserRepository.parse_user_orm_to_user(res, False)
                )
            return domain_result
        except SQLAlchemyError as e:
            await self.session.rollback()
            raise DatabaseConnectionException(e)

    async def get_user(self, user_id: uuid.UUID) -> User:
        try:
            stmt = select(UserORM).where(UserORM.id == user_id)

            result = await self.session.execute(stmt)
            if res := result.scalar():
                return SqlAlchemyUserRepository.parse_user_orm_to_user(res, False)
            raise UserNotFoundException
        except SQLAlchemyError as e:
            raise DatabaseConnectionException(e)

    async def get_user_by_filter(self, filter: str) -> User:
        try:
            result = await self.session.execute(
                select(UserORM).where(
                    or_(
                        UserORM.email == filter,
                        UserORM.username == filter,
                        UserORM.phone_number == filter,
                    )
                )
            )

            if res := result.scalar():
                return SqlAlchemyUserRepository.parse_user_orm_to_user(res, True)
            raise UserNotFoundException
        except SQLAlchemyError as e:
            raise DatabaseConnectionException(e)

    async def delete_user(self, user_id: uuid.UUID):
        try:
            stmt = delete(UserORM).where(UserORM.id == user_id)
            result = await self.session.execute(stmt)

            return result.rowcount
        except SQLAlchemyError as e:
            await self.session.rollback()
            raise DatabaseConnectionException(e)

    async def add_image(self, user_id: uuid.UUID, image_path: str) -> str:
        try:
            stmt = select(UserORM).where(UserORM.id == user_id)

            result = await self.session.execute(stmt)
            user = result.scalars().first()

            if user is None:
                raise UserNotFoundException

            user.image_s3_path = image_path
            await self.session.flush()
            return user.image_s3_path
        except SQLAlchemyError as e:
            raise DatabaseConnectionException(e)

    @staticmethod
    def parse_user_orm_to_user(user_db: UserORM, is_pwd: bool) -> User:
        user = User(
            id=user_db.id,
            name=user_db.name,
            surname=user_db.surname,
            username=user_db.username,
            phone_number=user_db.phone_number,
            email=user_db.email,
            role=user_db.role,
            group=user_db.group,
            image_path=user_db.image_s3_path,
            is_blocked=user_db.is_blocked,
        )

        if is_pwd is True:
            user.password = user_db.password

        return user
