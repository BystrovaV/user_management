import uuid
from typing import Annotated

from fastapi import APIRouter, Depends, UploadFile

from dependencies.dependencies import (
    check_file_format,
    delete_user_use_case,
    get_current_user,
    get_upload_image_use_case,
    get_user_use_case,
    update_user_use_case,
)
from domain.user import User
from routes.controllers import UserChange, UserOutput
from usecase.user_usecase import (
    DeleteUserUseCase,
    GetUserUseCase,
    UpdateUserUseCase,
    UploadImageUseCase,
)

router = APIRouter(
    prefix="/user",
    tags=["user"],
)


@router.get("/me", response_model=UserOutput)
async def get_user(user: Annotated[User, Depends(get_current_user)]):
    return user


@router.post("/me/image")
async def add_user_image(
    image: Annotated[UploadFile, Depends(check_file_format)],
    user: Annotated[User, Depends(get_current_user)],
    use_case: Annotated[UploadImageUseCase, Depends(get_upload_image_use_case)],
):
    return await use_case(image.file, image.filename, user)


@router.patch("/me")
async def patch_me(
    user_data: UserChange,
    user: Annotated[User, Depends(get_current_user)],
    use_case: Annotated[UpdateUserUseCase, Depends(update_user_use_case)],
):
    return await use_case(user, user.id, user_data.to_entity())


@router.delete("/me")
async def delete_user(
    user: Annotated[User, Depends(get_current_user)],
    use_case: Annotated[DeleteUserUseCase, Depends(delete_user_use_case)],
):
    return await use_case(user.id)


@router.get("/{user_id}", response_model=UserOutput)
async def get_user(
    user_id: uuid.UUID,
    current_user: Annotated[User, Depends(get_current_user)],
    use_case: Annotated[GetUserUseCase, Depends(get_user_use_case)],
):
    user = await use_case(user_id, current_user.group.id, current_user.role)
    return user


@router.patch("/{user_id}")
async def patch_user(
    user_id: uuid.UUID,
    user_data: UserChange,
    current_user: Annotated[User, Depends(get_current_user)],
    use_case: Annotated[UpdateUserUseCase, Depends(update_user_use_case)],
):
    return await use_case(current_user, user_id, user_data.to_entity())
