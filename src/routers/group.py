import logging
from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app import service
from app.models import get_session
from app.schemas import GroupBase

router = APIRouter(
    prefix="/group",
    tags=["group"],
)

logger = logging.getLogger(__name__)
SessionDependency = Annotated[AsyncSession, Depends(get_session)]


@router.post("")
async def add_group(group: GroupBase, session: SessionDependency):
    group = service.insert_group(session, group.name)

    try:
        await session.commit()
        logger.info(group)
        return group
    except IntegrityError as ex:
        await session.rollback()
        logger.error("The user is already stored")
        return "The user is already stored"


@router.get("")
async def get_groups(session: SessionDependency):
    groups = await service.get_groups(session)
    return groups


@router.get("/{group_id}")
async def get_group(group_id: int, session: SessionDependency):
    group = await service.get_group(session, group_id)
    return group
