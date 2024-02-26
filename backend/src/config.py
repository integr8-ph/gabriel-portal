from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    PROJECT_NAME: str
    DATABASE_URL: str
    TEST_DATABASE_URL: str
    COLLECTION_NAME: str
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_EXPIRE_TOKEN: int

    class Config:
        env_file = ".env"
        extra = "allow"


settings = Settings()


@lru_cache
def get_settings() -> Settings:
    return settings
