from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    DB_NAME: str = None
    DB_USER: str = None

    DB_PASSWORD: SecretStr = None
    DB_HOST: str = None
    DB_PORT: int = None

    ENV_STATE: str = None

    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", extra="allow"
    )

    @property
    def get_db_url(self):
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASSWORD.get_secret_value()}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"


# class Production(Settings):

#     class Config:
#         env_prefix: str = "PROD_"


# class Development(Settings):

#     class Config:
#         env_prefix: str = "DEV_"


# class FactorySettings:
#     """Returns a config instance dependending on the ENV_STATE variable."""

#     def __init__(self, env_state: Optional[str]):
#         self.env_state = env_state

#     def __call__(self):
#         if self.env_state == "DEVELOPMENT":
#             return Development()

#         elif self.env_state == "PRODUCTION":
#             return Production()
