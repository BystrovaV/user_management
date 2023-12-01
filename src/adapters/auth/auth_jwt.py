import logging
import uuid
from datetime import UTC, datetime, timedelta

import jwt

from core.exceptions import AuthorizationException
from core.settings import Settings
from ports.repositories.auth_service import AuthService

logger = logging.getLogger(__name__)


class JwtAuth(AuthService):
    def __init__(self, settings: Settings):
        self.settings = settings

    def create_token(self, user_id: uuid.UUID) -> str:
        payload = {
            "user_id": str(user_id),
            "exp": datetime.now(UTC) + timedelta(minutes=30),
        }

        token = jwt.encode(payload=payload, key=self.settings.get_jwt_secret)

        return token

    def parse_token(self, token) -> dict:
        try:
            payload = jwt.decode(
                jwt=token, key=self.settings.get_jwt_secret, algorithms=["HS256"]
            )

            return payload
        except jwt.PyJWTError as e:
            logger.exception(e)
            raise AuthorizationException
