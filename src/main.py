from fastapi import FastAPI

from src.database import db_init
from src.api import router
from src.config import get_settings

app = FastAPI(on_startup=[db_init], title=get_settings().PROJECT_NAME)

app.include_router(router)
