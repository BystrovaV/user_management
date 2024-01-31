import logging

from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from adapters.orm_engines.models import GroupORM
from core.exceptions import DatabaseConnectionException
from domain.group import Group
from ports.repositories.group_repository import GroupRepository

logger = logging.getLogger(__name__)


class SqlAlchemyGroupRepository(GroupRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_groups(self) -> list[Group]:
        try:
            stmt = select(GroupORM)
            result = await self.session.execute(stmt)

            domain_result = []
            for res in result.scalars().all():
                domain_result.append(
                    SqlAlchemyGroupRepository.parse_group_orm_to_group(res)
                )
            return domain_result
        except SQLAlchemyError as e:
            logger.exception(e)
            raise DatabaseConnectionException

    @staticmethod
    def parse_group_orm_to_group(group_db: GroupORM) -> Group:
        return Group(id=group_db.id, name=group_db.name)
