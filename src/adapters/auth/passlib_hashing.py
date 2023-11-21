from passlib.context import CryptContext

from core.exceptions import InvalidArgumentsException
from ports.repositories.password_hashing import PasswordHashing


class PasslibHashing(PasswordHashing):
    def __init__(self):
        self.pwd_context = CryptContext(schemes=["bcrypt"])

    def hash_password(self, password: str) -> str:
        try:
            hash_pwd = self.pwd_context.hash(password)
            return hash_pwd
        except (ValueError, TypeError):
            raise InvalidArgumentsException

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        try:
            is_verified = self.pwd_context.verify(plain_password, hashed_password)
            return is_verified
        except (ValueError, TypeError):
            raise InvalidArgumentsException
