import os
from beanie import init_beanie
import pytest_asyncio

from motor.motor_asyncio import AsyncIOMotorClient

from src.models import gather_models
from src.config import get_settings

from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

os.environ["DATABASE_URL"] = os.getenv("TEST_DATABASE_URL")

from src.main import app  # noqa


@pytest_asyncio.fixture()
async def clear_test_database():
    client = AsyncIOMotorClient(os.getenv("TEST_DATABASE_URL"))
    test_db = client[get_settings().COLLECTION_NAME]

    await init_beanie(test_db, document_models=gather_models())

    yield None

    collections = await test_db.list_collection_names()
    for collection in collections:
        await test_db[collection].drop()
