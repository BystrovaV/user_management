from enum import Enum

from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class EnvironmentTypes(Enum):
    test: str = "test"
    local: str = "local"


class Settings(BaseSettings):
    ENVIRONMENT: EnvironmentTypes = EnvironmentTypes.local

    DB_NAME: str = None
    DB_USER: str = None

    DB_PASSWORD: SecretStr = None
    DB_HOST: str = None
    DB_PORT: int = None

    REDIS_HOST: str = None
    REDIS_PORT: int = None

    JWT_SECRET: SecretStr = None
    BUCKET_NAME: str = None

    AWS_ACCESS_KEY_ID: str = None
    AWS_SECRET_ACCESS_KEY: str = None

    RABBIT_HOST: str
    RABBIT_PORT: int
    RABBIT_USER: str
    RABBIT_PASSWORD: str

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

    REDIS_HOST: str | None = None
    REDIS_PORT: int | None = None

    JWT_SECRET: SecretStr = "cf6b56353597d5a0cd253b57b5cea25fd689f433ce3b40f5"
    BUCKET_NAME: str | None = None

    AWS_ACCESS_KEY_ID: str | None = None
    AWS_SECRET_ACCESS_KEY: str | None = None

    RABBIT_HOST: str | None = None
    RABBIT_PORT: int | None = None
    RABBIT_USER: str | None = None
    RABBIT_PASSWORD: str | None = None


environments = {
    EnvironmentTypes.test: TestSettings,
    EnvironmentTypes.local: Settings,
}


def get_settings() -> Settings:
    app_env = Settings().environment
    return environments[app_env]()


# def get_settings():
#     return Settings()
