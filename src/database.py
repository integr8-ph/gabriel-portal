from contextlib import asynccontextmanager
from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie

from src.config import get_settings
from src.models import gather_models


@asynccontextmanager
async def db_init():
    try:
        client = AsyncIOMotorClient(get_settings().DATABASE_URL)
        await init_beanie(
            database=client[get_settings().COLLECTION_NAME],
            document_models=gather_models(),
        )
        yield
    except Exception as e:
        raise RuntimeError("Failed to connect to the database.") from e
