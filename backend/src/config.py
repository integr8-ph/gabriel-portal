from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    ENVIRONMENT: str
    PROJECT_NAME: str
    DATABASE_URL: str
    TEST_DATABASE_URL: str
    COLLECTION_NAME: str
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_EXPIRE_TOKEN: int


@lru_cache
def get_settings() -> Settings:
    return Settings()
