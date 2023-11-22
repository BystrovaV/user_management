import uuid

from ports.repositories.auth_service import AuthService


class InMemoryAuth(AuthService):
    def __init__(self):
        self.tokens = {}

    def create_token(self, user_id: uuid.UUID) -> str:
        token = uuid.uuid4().hex
        self.tokens[token] = user_id
        return token

    def parse_token(self, token) -> dict:
        return {"user_id": self.tokens[token]}
