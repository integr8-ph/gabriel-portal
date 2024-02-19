from contextlib import asynccontextmanager

from fastapi import FastAPI
from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie

from src.auth.models import UserCreate


@asynccontextmanager
async def db_init(app: FastAPI):
    try:
        client = AsyncIOMotorClient("mongodb://127.0.0.1:27017")
        await init_beanie(database=client["testdb"], document_models=[UserCreate])
        print("Successfully connected to the database.")
        yield
    except Exception as e:
        raise RuntimeError("Failed to connect to the database.") from e
