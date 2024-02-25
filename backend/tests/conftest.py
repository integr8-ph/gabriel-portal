import os
from typing import AsyncIterator
import pytest_asyncio

from httpx import AsyncClient
from asgi_lifespan import LifespanManager
from motor.motor_asyncio import AsyncIOMotorClient

from src.auth.dependencies import get_current_active_superuser

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


@pytest_asyncio.fixture(autouse=True)
async def clear_test_database():
    client = AsyncIOMotorClient(TEST_DATABASE_URL)
    test_db = client["portal"]

    yield None

    collections = await test_db.list_collection_names()
    for collection in collections:
        await test_db[collection].drop()


async def skip_oauth2() -> None:
    pass


app.dependency_overrides[get_current_active_superuser] = skip_oauth2


@pytest_asyncio.fixture
async def client() -> AsyncIterator[AsyncClient]:
    async with LifespanManager(app):
        async with AsyncClient(app=app, base_url="http://test") as async_client:
            yield async_client
