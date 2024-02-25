import os
from beanie import init_beanie
import pytest_asyncio

from motor.motor_asyncio import AsyncIOMotorClient

from src.models import gather_models
from src.config import get_settings

from pathlib import Path
from dotenv import load_dotenv, find_dotenv

CURRENT_DIRECTORY = Path(__file__).resolve().parent.parent
TEST_DATABASE_URL = "mongodb+srv://yukokunomoriarty:xmsJjbqpSQ0h1X6y@home-security-neko.ovbtlac.mongodb.net/"

try:
    load_dotenv(CURRENT_DIRECTORY / ".env")
except Exception:
    load_dotenv(find_dotenv())

os.environ["DATABASE_URL"] = TEST_DATABASE_URL

from src.main import app  # noqa


@pytest_asyncio.fixture()
async def clear_test_database():
    client = AsyncIOMotorClient(TEST_DATABASE_URL)
    test_db = client[get_settings().COLLECTION_NAME]

    await init_beanie(test_db, document_models=gather_models())

    yield None

    collections = await test_db.list_collection_names()
    for collection in collections:
        await test_db[collection].drop()
