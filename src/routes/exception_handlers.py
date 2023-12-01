from fastapi import Request, status
from fastapi.responses import JSONResponse

from core.exceptions import *


async def user_not_found_exception_handler(
    request: Request, exc: UserNotFoundException
):
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={"message": "User not found"},
    )


async def database_exception_handler(
    request: Request, exc: DatabaseConnectionException
):
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"message": "Something get wrong in database"},
    )


async def user_exists_exception_handler(
    request: Request, exc: UserAlreadyExistsException
):
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={"message": "User with such credentials is already exists"},
    )


async def authentication_exception_handler(
    request: Request, exc: AuthenticationException
):
    return JSONResponse(
        status_code=status.HTTP_401_UNAUTHORIZED,
        content={"message": "Cannot authenticate you. Check your password"},
    )


async def authorization_exception_handler(
    request: Request, exc: AuthorizationException
):
    return JSONResponse(
        status_code=status.HTTP_401_UNAUTHORIZED,
        content={"message": "Cannot authorize you"},
    )


async def access_denied_exception_handler(request: Request, exc: AccessDenied):
    return JSONResponse(
        status_code=status.HTTP_403_FORBIDDEN,
        content={"message": "You have no enough permissions"},
    )


async def token_denied_exception_handler(request: Request, exc: TokenDenied):
    return JSONResponse(
        status_code=status.HTTP_401_UNAUTHORIZED,
        content={"message": "This token is not available anymore"},
    )


async def redis_connection_exception(request: Request, exc: RedisConnectionException):
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"message": "Redis connection is failed"},
    )


async def invalid_image_exception(request: Request, exc: InvalidImageException):
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={"message": "Input should be a valid image"},
    )


async def localstack_exception(request: Request, exc: LocalStackConnectionException):
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"message": "Localsyack connection failed"},
    )


async def user_is_blocked_exception(request: Request, exc: UserIsBlockedException):
    return JSONResponse(
        status_code=status.HTTP_403_FORBIDDEN,
        content={"message": "You are blocked"},
    )


async def message_delivery_exception(request: Request, exc: MessageDeliveryException):
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "message": "Sorry, It is not possible to deliver a message to you at the moment"
        },
    )
