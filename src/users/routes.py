from typing import Annotated
from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm

from src.auth.dependencies import (
    authenticate_user,
    create_access_token,
    get_current_active_user,
)
from src.auth.exceptions import InvalidUserOrPass
from src.auth.schemas import Token
from src.config import get_settings
from src.users.schemas import UserCreate, UserOut
from src.users.services import create_user, get_user_by_email
from src.exceptions import Conflict

router = APIRouter()


@router.post("/login/access-token")
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()]
) -> Token:
    user = await authenticate_user(form_data.username, form_data.password)

    if not user:
        raise InvalidUserOrPass()

    access_token_expires = get_settings().ACCESS_EXPIRE_TOKEN

    access_token = await create_access_token(user.username, access_token_expires)

    return Token(access_token=access_token, token_type="bearer")


@router.post(
    "/signup",
    response_model=UserOut,
)
async def signup(user: UserCreate) -> UserOut:
    new_user = await get_user_by_email(user.email)

    if new_user:
        raise Conflict()

    new_user = await create_user(user=user)

    return new_user
