import os
from typing import Annotated
from datetime import datetime, timedelta, timezone

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from jose import jwt, JWTError
from dotenv import load_dotenv

from src.auth.schemas import User, TokenData
from src.auth.models import UserCreate
from src.auth.exceptions import InactiveUser, NotAuthenticated
from src.auth.constants import ENV_PATH


password_context = CryptContext(schemes=["bcrypt"])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/token")

load_dotenv(dotenv_path=ENV_PATH)


async def get_user_in_db(username: str) -> User:
    user = await UserCreate.find(UserCreate.username == username).to_list()
    if user:
        return user[0]

    return None


def verify_password(plain_password: str, hashed_password) -> bool:
    return password_context.verify(plain_password, hashed_password)


def get_hashed_password(password: str) -> str:
    return password_context.hash(password)


async def authenticate_user(username: str, password: str) -> User | bool:
    user = await get_user_in_db(username)

    if not user:
        return False

    if not verify_password(password, user.password):
        return False

    return user


async def create_access_token(data: dict, expire_time: timedelta | None = None) -> str:
    data_to_encode = data.copy()

    if expire_time:
        expire = datetime.now(timezone.utc) + expire_time
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=30)

    data_to_encode["exp"] = expire
    encoded_jwt = jwt.encode(
        data_to_encode, os.getenv("SECRET_KEY"), algorithm=os.getenv("ALGORITHM")
    )

    return encoded_jwt


async def decode_token(token) -> User:
    user = await get_user_in_db(token)
    return user


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]) -> User:
    try:
        payload = jwt.decode(
            token, os.getenv("SECRET_KEY"), algorithms=[os.getenv("ALGORITHM")]
        )
        username: str = payload.get("sub")
        if not username:
            raise NotAuthenticated()

        token_data = TokenData(username=username)
    except JWTError:
        raise NotAuthenticated()

    user = await get_user_in_db(username=token_data.username)

    if not user:
        raise NotAuthenticated()

    return user


async def get_current_active_user(
    current_user: Annotated[User, Depends(get_current_user)]
) -> User:
    if not current_user:
        raise InactiveUser()

    return current_user
