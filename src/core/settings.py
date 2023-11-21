from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    DB_NAME: str = None
    DB_USER: str = None

    DB_PASSWORD: SecretStr = None
    DB_HOST: str = None
    DB_PORT: int = None

    REDIS_HOST: str = None
    REDIS_PORT: int = None

    JWT_SECRET: SecretStr = None
    # JWT_ALGORITHM: str = None

    # ENV_STATE: str = None
    # env_file="../.env",
    model_config = SettingsConfigDict(extra="allow")

    @property
    def get_db_url(self):
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASSWORD.get_secret_value()}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    @property
    def get_redis_url(self):
        return f"redis://{self.REDIS_HOST}:{self.REDIS_PORT}"

    @property
    def get_jwt_secret(self):
        # print(self.JWT_SECRET.get_secret_value())
        return self.JWT_SECRET.get_secret_value()
