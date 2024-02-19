from typing import Annotated

from fastapi import FastAPI, Depends

from src.database import db_init

from src.auth.schemas import User, UserNoPassword
from src.auth.models import UserCreate
from src.auth.dependencies import get_current_active_user, get_hashed_password
from src.auth import router

app = FastAPI(lifespan=db_init)

app.include_router(router.router)


@app.get("/")
async def index():
    return "Index"


@app.get("/user")
async def get_user(
    user: Annotated[User, Depends(get_current_active_user)]
) -> UserNoPassword:
    return user


@app.post("/users")
async def create_user(user: User) -> User:
    hashed_password = get_hashed_password(user.password)
    user_create = UserCreate(username=user.username, password=hashed_password)
    await user_create.create()
    return user_create
