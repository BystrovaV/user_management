from typing import Annotated

from fastapi import APIRouter, Depends

from dependencies.dependencies import (
    get_login_use_case,
    get_refresh_token_use_case,
    get_reset_password_use_case,
    get_signup_use_case,
    oauth2_scheme,
)
from routes.controllers import EmailBase, UserInput, UserLogin
from usecase.auth_usecase import (
    LoginUseCase,
    RefreshTokenUseCase,
    ResetPasswordUseCase,
    SignupUseCase,
)

router = APIRouter(
    prefix="/auth",
    tags=["auth"],
)


@router.post("/login")
async def login_for_access_token(
    user_data: UserLogin, use_case: Annotated[LoginUseCase, Depends(get_login_use_case)]
):
    token = await use_case(user_data.model_dump())
    return token


@router.post("/signup")
async def signup(
    user: UserInput, use_case: Annotated[SignupUseCase, Depends(get_signup_use_case)]
):
    return await use_case(user.to_entity())


@router.post("/refresh-token")
async def refresh_token(
    token: Annotated[str, Depends(oauth2_scheme)],
    use_case: Annotated[RefreshTokenUseCase, Depends(get_refresh_token_use_case)],
):
    return await use_case(token)


@router.post("/reset-password")
async def reset_password(
    email: EmailBase,
    use_case: Annotated[ResetPasswordUseCase, Depends(get_reset_password_use_case)],
):
    await use_case(email.email)
