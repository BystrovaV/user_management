class UserNotFoundException(Exception):
    pass


class DatabaseConnectionException(Exception):
    pass


class UserIsAlreadyExistsException(Exception):
    pass


class AuthenticationException(Exception):
    pass


class AuthorizationException(Exception):
    pass


class AccessDenied(Exception):
    pass


class TokenDenied(Exception):
    pass
