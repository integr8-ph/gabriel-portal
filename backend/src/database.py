from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie

from src.config import get_settings
from src.models import gather_models


async def db_init() -> None:
    client = AsyncIOMotorClient(get_settings().DATABASE_URL)
    await init_beanie(client["portal"], document_models=gather_models())
