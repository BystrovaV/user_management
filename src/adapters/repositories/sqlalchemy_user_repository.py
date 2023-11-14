from sqlalchemy import delete, desc, select
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from adapters.orm_engines.models import UserORM
from core.exceptions import (
    DatabaseConnectionException,
    UserIsAlreadyExistsException,
    UserNotFoundException,
)
from domain.user import User
from ports.repositories.user_repository import UserRepository


class SqlAlchemyUserRepository(UserRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def save_user(self, user: User) -> int:
        try:
            new_user = UserORM(
                name=user.name,
                surname=user.surname,
                username=user.username,
                phone_number=user.phone_number,
                email=user.email,
                role=user.role,
                group=user.group.id,
                password=user.password,
            )

            self.session.add(new_user)
            await self.session.commit()
            await self.session.refresh(new_user)
            return new_user.id
        except IntegrityError as e:
            await self.session.rollback()
            raise UserIsAlreadyExistsException
        except Exception as e:
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
                    User(
                        id=res.id,
                        name=res.name,
                        surname=res.surname,
                        username=res.username,
                        phone_number=res.phone_number,
                        email=res.email,
                        role=res.role,
                        group=res.group,
                    )
                )
            return domain_result
        except Exception as e:
            await self.session.rollback()
            raise DatabaseConnectionException(e)

    async def get_user(self, user_id: int) -> User:
        try:
            stmt = select(UserORM).where(UserORM.id == user_id)

            result = await self.session.execute(stmt)
            if res := result.scalar():
                return User(
                    id=res.id,
                    name=res.name,
                    surname=res.surname,
                    username=res.username,
                    phone_number=res.phone_number,
                    email=res.email,
                    role=res.role,
                    group=res.group,
                )
            raise UserNotFoundException
        except SQLAlchemyError as e:
            await self.session.rollback()
            raise DatabaseConnectionException(e)

    async def get_user_by_username(self, username: str) -> User:
        try:
            result = await self.session.execute(
                select(UserORM).where(UserORM.username == username)
            )

            if res := result.scalar():
                return User(
                    id=res.id,
                    name=res.name,
                    surname=res.surname,
                    username=res.username,
                    password=res.password,
                    phone_number=res.phone_number,
                    email=res.email,
                    role=res.role,
                    group=res.group,
                )
            raise UserNotFoundException
        except SQLAlchemyError as e:
            await self.session.rollback()
            raise DatabaseConnectionException(e)

    async def get_user_by_email(self, email: str) -> User:
        try:
            result = await self.session.execute(
                select(UserORM).where(UserORM.email == email)
            )

            if res := result.scalar():
                return User(
                    id=res.id,
                    name=res.name,
                    surname=res.surname,
                    username=res.username,
                    password=res.password,
                    phone_number=res.phone_number,
                    email=res.email,
                    role=res.role,
                    group=res.group,
                )
            raise UserNotFoundException
        except SQLAlchemyError as e:
            await self.session.rollback()
            raise DatabaseConnectionException(e)

    async def get_user_by_phone_number(self, phone_number: str) -> User:
        try:
            result = await self.session.execute(
                select(UserORM).where(UserORM.phone_number == phone_number)
            )

            if res := result.scalar():
                return User(
                    id=res.id,
                    name=res.name,
                    surname=res.surname,
                    username=res.username,
                    password=res.password,
                    phone_number=res.phone_number,
                    email=res.email,
                    role=res.role,
                    group=res.group,
                )
            raise UserNotFoundException
        except SQLAlchemyError as e:
            await self.session.rollback()
            raise DatabaseConnectionException(e)

    async def delete_user(self, user_id: int):
        try:
            stmt = delete(UserORM).where(UserORM.id == user_id)
            result = await self.session.execute(stmt)

            if result.rowcount:
                await self.session.commit()

            return result.rowcount

        except Exception as e:
            await self.session.rollback()
            raise DatabaseConnectionException(e)

    async def update_user(self, user_id: int, user_data: dict) -> User:
        try:
            stmt = select(UserORM).where(UserORM.id == user_id)
            user = (await self.session.execute(stmt)).scalar()

            if user is None:
                raise UserNotFoundException

            if user_data.get("name"):
                user.name = user_data.get("name")

            if user_data.get("surname"):
                user.surname = user_data.get("surname")

            if user_data.get("username"):
                user.username = user_data.get("username")

            if user_data.get("email"):
                user.email = user_data.get("email")

            if user_data.get("phone_number"):
                user.phone_number = user_data.get("phone_number")

            await self.session.commit()
            return User(
                id=user.id,
                name=user.name,
                surname=user.surname,
                username=user.username,
                phone_number=user.phone_number,
                email=user.email,
                role=user.role,
                group=user.group,
            )

        # except UserNotFoundException:
        #     raise UserNotFoundException
        except IntegrityError as e:
            await self.session.rollback()
            raise UserIsAlreadyExistsException
        except SQLAlchemyError as e:
            print("database exception")
            await self.session.rollback()
            raise DatabaseConnectionException(e)
