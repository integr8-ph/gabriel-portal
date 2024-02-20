import os
from typing import Annotated
from datetime import timedelta

from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from dotenv import load_dotenv

from src.auth.dependencies import create_access_token, authenticate_user
from src.auth.exceptions import InvalidUserOrPass
from src.auth.constants import ENV_PATH
from src.auth.schemas import Token
from src.config import get_settings

router = APIRouter()
load_dotenv(dotenv_path=ENV_PATH)


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
