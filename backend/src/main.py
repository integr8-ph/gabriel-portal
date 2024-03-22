from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.database import db_init
from src.api import router
from src.config import get_settings

app = FastAPI(lifespan=db_init, title=get_settings().PROJECT_NAME)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)
