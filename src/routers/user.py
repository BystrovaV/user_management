from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app import service
from app.auth_service import get_current_user
from app.models import RoleEnum, User, get_session

router = APIRouter(
    prefix="/user",
    tags=["user"],
)

SessionDependency = Annotated[AsyncSession, Depends(get_session)]


@router.get("/me")
async def get_user(current_user: Annotated[User, Depends(get_current_user)]):
    return current_user


@router.delete("/me")
async def delete_user(
    current_user: Annotated[User, Depends(get_current_user)], session: SessionDependency
):
    result = await service.delete_user(session, current_user.id)
    if result:
        return "Deleted successfully!"


@router.get("/{user_id}")
async def get_user(
    current_user: Annotated[User, Depends(get_current_user)],
    session: SessionDependency,
    user_id: int,
):
    user = await service.get_user(session, user_id)
    return user


# @router.delete("/{user_id}")
# async def delete_user(user_id: int, session: SessionDependency):
#     result = await service.delete_user(session, user_id)
#     if result:
#         return "Deleted successfully!"
