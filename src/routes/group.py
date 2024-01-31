from typing import Annotated

from fastapi import APIRouter, Depends

from dependencies.dependencies import get_groups_use_case
from routes.controllers import GroupOutput
from usecase.group_usecase import GetGroupsUseCase

router = APIRouter(
    prefix="/groups",
    tags=["group"],
)


@router.get("", response_model=list[GroupOutput])
async def get_groups(
    use_case: Annotated[GetGroupsUseCase, Depends(get_groups_use_case)]
):
    return await use_case()
