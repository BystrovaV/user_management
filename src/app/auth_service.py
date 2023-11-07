import time
from typing import Annotated

import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import User, get_session
from app.service import get_user, get_user_by_username
from app.settings import Settings

settings = Settings()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


def create_access_token(user_id: int):
    payload = {"user_id": user_id, "expires": time.time() + 600}

    token = jwt.encode(
        payload=payload,
        key=settings.get_jwt_secret
        # algorithm=settings.JWT_ALGORITHM
    )

    return token


async def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)],
    session: Annotated[AsyncSession, Depends(get_session)],
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(
            jwt=token, key=settings.get_jwt_secret, algorithms=["HS256"]
        )
        user_id: int = payload.get("user_id")

        if user_id is None:
            raise credentials_exception

    except jwt.PyJWTError:
        raise credentials_exception

    user = await get_user(session, user_id)
    if user is None:
        raise credentials_exception

    return user


async def authenticate_user(username: str, password: str, session: AsyncSession):
    user = await get_user_by_username(session, username)
    if not user:
        return False

    # ------------------------------
    # if not verify_password(password, user.hashed_password):
    #     return False
    return user


# class PermissionsRouter:
#     def __init__(self, permissions: tuple):
#         self.permissions = permissions

#     def check_access(self, current_user: User):
#         for permission in current_user.permissions:
#             if permission.code_name in self.permissions:
#                 return current_user

#         raise HTTPException(status_code=400, detail="The user doesn't have enough privileges")

#     def __call__(self, user: User = Depends(get_current_user)):
#         return self.check_access(current_user=user)
