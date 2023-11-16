from fastapi import Request, status
from fastapi.responses import JSONResponse

from core.exceptions import *


# @app.exception_handler(UserNotFoundException)
async def user_not_found_exception_handler(
    request: Request, exc: UserNotFoundException
):
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={"message": "User not found"},
    )


# @app.exception_handler(DatabaseConnectionException)
async def database_exception_handler(
    request: Request, exc: DatabaseConnectionException
):
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"message": "Something get wrong in database"},
    )


# @app.exception_handler(UserAlreadyExistsException)
async def user_exists_exception_handler(
    request: Request, exc: UserAlreadyExistsException
):
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={"message": "User with such credentials is already exists"},
    )


# @app.exception_handler(AuthenticationException)
async def authentication_exception_handler(
    request: Request, exc: AuthenticationException
):
    return JSONResponse(
        status_code=status.HTTP_401_UNAUTHORIZED,
        content={"message": "Cannot authenticate you. Check your password"},
    )


# @app.exception_handler(AuthorizationException)
async def authorization_exception_handler(
    request: Request, exc: AuthorizationException
):
    return JSONResponse(
        status_code=status.HTTP_401_UNAUTHORIZED,
        content={"message": "Cannot authorize you"},
    )


# @app.exception_handler(AccessDenied)
async def access_denied_exception_handler(request: Request, exc: AccessDenied):
    return JSONResponse(
        status_code=status.HTTP_403_FORBIDDEN,
        content={"message": "You have no enough permissions"},
    )


# @app.exception_handler(TokenDenied)
async def token_denied_exception_handler(request: Request, exc: TokenDenied):
    return JSONResponse(
        status_code=status.HTTP_401_UNAUTHORIZED,
        content={"message": "This token is not available anymore"},
    )


# @app.exception_handler(RedisConnectionException)
async def redis_connection_exception(request: Request, exc: RedisConnectionException):
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"message": "Redis connection is failed"},
    )
