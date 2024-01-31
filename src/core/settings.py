from enum import Enum
from functools import lru_cache

from pydantic import Field, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class EnvironmentTypes(Enum):
    test: str = "test"
    local: str = "local"
    prod: str = "prod"


class Settings(BaseSettings):
    environment: EnvironmentTypes = Field(
        EnvironmentTypes.local, env="USER_MANAGEMENT_ENVIRONMENT"
    )

    DB_NAME: str = "UserManagement"
    DB_USER: str = "root"

    DB_PASSWORD: SecretStr
    DB_HOST: str = "localhost"
    DB_PORT: int = 5432

    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6380

    JWT_SECRET: SecretStr
    BUCKET_NAME: str

    AWS_ACCESS_KEY_ID: str = "test"
    AWS_SECRET_ACCESS_KEY: str = "test"

    RABBIT_HOST: str = "localhost"
    RABBIT_PORT: int = 5672
    RABBIT_USER: str = "root"
    RABBIT_PASSWORD: str = "1234567"
    RABBIT_EMAIL_QUEUE: str = "reset_password"

    model_config = SettingsConfigDict(extra="allow")

    @property
    def get_db_url(self):
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASSWORD.get_secret_value()}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    @property
    def get_redis_url(self):
        return f"redis://{self.REDIS_HOST}:{self.REDIS_PORT}"

    @property
    def get_jwt_secret(self):
        return self.JWT_SECRET.get_secret_value()

    def get_image_url(self, key_name: str):
        return (
            f"http://{self.BUCKET_NAME}.s3.localhost.localstack.cloud:4566/{key_name}"
        )

    def get_localstack_endpoint(self):
        return "http://localhost.localstack.cloud:4566"


class TestSettings(Settings):
    DB_NAME: str = "TestUserManagement"
    DB_USER: str = "test"

    DB_PASSWORD: SecretStr = "test"
    DB_HOST: str = "localhost"
    DB_PORT: int = 5432

    JWT_SECRET: SecretStr = "cf6b56353597d5a0cd253b57b5cea25fd689f433ce3b40f5"
    BUCKET_NAME: str | None = None


class LocalSettings(Settings):
    pass


class ProdSettings(Settings):
    pass


environments = {
    EnvironmentTypes.test: TestSettings,
    EnvironmentTypes.local: LocalSettings,
    EnvironmentTypes.prod: ProdSettings,
}


@lru_cache
def get_settings() -> Settings:
    app_env = Settings().environment
    return environments[app_env]()
