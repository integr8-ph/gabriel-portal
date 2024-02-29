from typing import Annotated
from datetime import datetime, timedelta, timezone

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from pydantic import EmailStr

from src.auth.schemas import TokenData
from src.auth.exceptions import InactiveUser, NotAuthenticated, NotSuperuser
from src.auth.services import verify_password
from src.config import get_settings
from src.users.models import User
from src.users.schemas import CreateOut
from src.users.services import get_user_by_email


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login/access-token")


async def authenticate_user(email: EmailStr, password: str) -> User | bool:
    user = await get_user_by_email(email)

    if not user:
        return False

    if not verify_password(
        plain_password=password, hashed_password=user.hashed_password
    ):
        return False

    return user


async def create_access_token(data: str, expire_time: int | None = None) -> str:
    access_expire_token = timedelta(expire_time)

    expire = datetime.now(timezone.utc) + access_expire_token

    payload = {"sub": data, "exp": expire}

    encoded_jwt = jwt.encode(
        payload, get_settings().SECRET_KEY, algorithm=get_settings().ALGORITHM
    )

    return encoded_jwt


TokenDep = Annotated[str, Depends(oauth2_scheme)]


async def get_current_user(token: TokenDep) -> User:
    try:
        payload = jwt.decode(
            token, get_settings().SECRET_KEY, algorithms=[get_settings().ALGORITHM]
        )

        email: str = payload.get("sub")

        if not email:
            raise NotAuthenticated()

        token_data = TokenData(email=email)
    except JWTError as e:
        raise e

    user = await get_user_by_email(email=token_data.email)

    if not user:
        raise NotAuthenticated()

    return user


CurrentUser = Annotated[User, Depends(get_current_user)]


async def get_current_active_user(current_user: CurrentUser) -> CreateOut:
    if not current_user.is_active:
        raise InactiveUser()

    return current_user


async def get_current_active_superuser(current_user: CurrentUser) -> CreateOut:
    if not current_user.is_superuser:
        raise NotSuperuser()

    return current_user
