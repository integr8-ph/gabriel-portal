from contextlib import asynccontextmanager
from typing import AsyncGenerator
from fastapi import FastAPI

from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie

from src.config import get_settings
from src.models import gather_models


@asynccontextmanager
async def db_init(app: FastAPI) -> AsyncGenerator[None, None]:
    if get_settings().ENVIRONMENT == "dev":
        client = AsyncIOMotorClient(get_settings().DATABASE_URL)
    else:
        client = AsyncIOMotorClient(get_settings().TEST_DATABASE_URL)

    await init_beanie(
        client[get_settings().COLLECTION_NAME], document_models=gather_models()
    )
    yield
