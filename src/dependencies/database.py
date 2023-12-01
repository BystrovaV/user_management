from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from adapters.orm_engines.sql_alchemy import SqlAlchemy
from core.settings import Settings, get_settings


class SqlAlchemyDependency:
    def __init__(self):
        self.sqlalchemy = None

    async def __call__(self, settings: Settings = Depends(get_settings)) -> SqlAlchemy:
        self.sqlalchemy = (
            SqlAlchemy.start(settings.get_db_url)
            if not self.sqlalchemy
            else self.sqlalchemy
        )
        return self.sqlalchemy


get_sql_alchemy = SqlAlchemyDependency()


async def get_session(
    sqlalchemy: SqlAlchemy = Depends(get_sql_alchemy),
) -> AsyncSession:
    async with sqlalchemy.session_maker() as session:
        async with session.begin():
            yield session
