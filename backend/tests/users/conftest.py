from typing import AsyncIterator
from beanie import init_beanie
import pytest_asyncio

from httpx import AsyncClient
from asgi_lifespan import LifespanManager
from motor.motor_asyncio import AsyncIOMotorClient

from src.models import gather_models
from src.auth.dependencies import get_current_active_superuser

from src.config import get_settings  # noqa
from src.main import app  # noqa


@pytest_asyncio.fixture(autouse=True)
async def clear_test_database():
    client = AsyncIOMotorClient(get_settings().TEST_DATABASE_URL)
    test_db = client[get_settings().COLLECTION_NAME]

    await init_beanie(test_db, document_models=gather_models())

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
