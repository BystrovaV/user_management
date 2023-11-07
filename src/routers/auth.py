from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app import service
from app.auth_service import authenticate_user, create_access_token
from app.models import get_session
from app.schemas import UserLogin

router = APIRouter(
    prefix="/auth",
    tags=["auth"],
)

SessionDependency = Annotated[AsyncSession, Depends(get_session)]


@router.post("/login")
async def login_for_access_token(form_data: UserLogin, session: SessionDependency):
    # ---------------------
    user = await authenticate_user(form_data.username, form_data.password, session)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = create_access_token(user.id)
    return {"access_token": access_token, "token_type": "bearer"}
