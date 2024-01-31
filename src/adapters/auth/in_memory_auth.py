import uuid

from domain.user import RoleEnum
from ports.repositories.auth_service import AuthService


class InMemoryAuth(AuthService):
    def __init__(self):
        self.tokens = {}

    def create_token(
        self, user_id: uuid.UUID, group_id: uuid.UUID, role: RoleEnum
    ) -> str:
        token = uuid.uuid4().hex
        self.tokens[token] = {
            "user_id": user_id,
            "token_type": "access",
        }
        return token

    def parse_token(self, token) -> dict:
        return self.tokens[token]

    def create_refresh_token(self, user_id: uuid.UUID) -> str:
        token = uuid.uuid4().hex
        self.tokens[token] = {
            "user_id": user_id,
            "token_type": "refresh",
        }
        return token
