class UserNotFoundException(Exception):
    pass


class DatabaseConnectionException(Exception):
    pass


class UserAlreadyExistsException(Exception):
    pass


class AuthenticationException(Exception):
    pass


class AuthorizationException(Exception):
    pass


class AccessDenied(Exception):
    pass


class TokenDenied(Exception):
    pass


class RedisConnectionException(Exception):
    pass


class InvalidArgumentsException(Exception):
    pass
