import logging

from fastapi import FastAPI

from routes.exception_handlers import *

app = FastAPI()

app.add_exception_handler(UserNotFoundException, user_not_found_exception_handler)
app.add_exception_handler(DatabaseConnectionException, database_exception_handler)
app.add_exception_handler(UserAlreadyExistsException, user_exists_exception_handler)
app.add_exception_handler(AuthenticationException, authentication_exception_handler)
app.add_exception_handler(AuthorizationException, authorization_exception_handler)
app.add_exception_handler(AccessDenied, access_denied_exception_handler)
app.add_exception_handler(TokenDenied, token_denied_exception_handler)
app.add_exception_handler(RedisConnectionException, redis_connection_exception)


logging.config.fileConfig("logging.conf", disable_existing_loggers=False)
logger = logging.getLogger(__name__)
