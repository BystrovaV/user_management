# import logging
import logging
from typing import Annotated

from fastapi import Depends, FastAPI, Request
from fastapi.responses import JSONResponse

from core.exceptions import *
from dependencies.dependencies import get_current_user, get_users_use_case
from domain.user import User
from routes.controllers import UsersQueryParams
from usecase.user_usecase import GetUsersUseCase

app = FastAPI()

logging.config.fileConfig("logging.conf", disable_existing_loggers=False)
logger = logging.getLogger(__name__)


@app.exception_handler(UserNotFoundException)
async def user_not_found_exception_handler(
    request: Request, exc: UserNotFoundException
):
    return JSONResponse(
        status_code=404,
        content={"message": "User not found"},
    )


@app.exception_handler(DatabaseConnectionException)
async def database_exception_handler(
    request: Request, exc: DatabaseConnectionException
):
    return JSONResponse(
        status_code=500,
        content={"message": "Something get wrong in database"},
    )


@app.exception_handler(UserIsAlreadyExistsException)
async def user_is_exists_exception_handler(
    request: Request, exc: UserIsAlreadyExistsException
):
    return JSONResponse(
        status_code=500,
        content={"message": "User with such credentials is already exists"},
    )


@app.exception_handler(AuthenticationException)
async def authentication_exception_handler(
    request: Request, exc: AuthenticationException
):
    return JSONResponse(
        status_code=401,
        content={"message": "Cannot authenticate you. Check your password"},
    )


@app.exception_handler(AuthorizationException)
async def authorization_exception_handler(
    request: Request, exc: AuthorizationException
):
    return JSONResponse(
        status_code=401,
        content={"message": "Cannot authorize you"},
    )


@app.exception_handler(AccessDenied)
async def access_denied_exception_handler(request: Request, exc: AccessDenied):
    return JSONResponse(
        status_code=403,
        content={"message": "You have no enough permissions"},
    )


@app.exception_handler(TokenDenied)
async def token_denied_exception_handler(request: Request, exc: TokenDenied):
    return JSONResponse(
        status_code=401,
        content={"message": "This token not available anymore"},
    )


@app.get("/users")
async def get_users(
    params: Annotated[UsersQueryParams, Depends()],
    use_case: Annotated[GetUsersUseCase, Depends(get_users_use_case)],
    user: Annotated[User, Depends(get_current_user)],
):
    users = await use_case(user.group.id, user.role, **params.model_dump())
    return users
