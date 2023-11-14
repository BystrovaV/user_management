import time
from datetime import datetime, timedelta

import jwt

from core.exceptions import AuthorizationException
from core.settings import Settings
from ports.repositories.auth_repository import AuthRepository


class JwtAuth(AuthRepository):
    def __init__(self, settings: Settings):
        self.settings = settings

    def create_token(self, user_id: int) -> str:
        payload = {"user_id": user_id, "exp": datetime.utcnow() + timedelta(minutes=30)}

        token = jwt.encode(payload=payload, key=self.settings.get_jwt_secret)

        return token

    def parse_token(self, token) -> dict:
        try:
            payload = jwt.decode(
                jwt=token, key=self.settings.get_jwt_secret, algorithms=["HS256"]
            )

            return payload
        except jwt.PyJWTError:
            raise AuthorizationException
