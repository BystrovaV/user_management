from typing import Annotated

from fastapi import APIRouter, Depends

from dependencies.dependencies import get_current_user, get_users_use_case
from domain.user import User
from routes.controllers import UserOutput, UsersQueryParams
from usecase.user_usecase import GetUsersUseCase

router = APIRouter(
    prefix="/users",
    tags=["users"],
)


@router.get("", response_model=list[UserOutput])
async def get_users(
    params: Annotated[UsersQueryParams, Depends()],
    use_case: Annotated[GetUsersUseCase, Depends(get_users_use_case)],
    user: Annotated[User, Depends(get_current_user)],
):
    users = await use_case(user.group.id, user.role, **params.model_dump())
    return users
