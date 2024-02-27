from typing import Optional

from pydantic import EmailStr
from src.auth.services import get_hashed_password

from src.users.models import User
from src.users.schemas import (
    DeleteOut,
    CreateOut,
    UpdateOut,
    UserCreate,
    UserUpdate,
)

from src.users.crud_class import CRUDBase


async def get_user_by_email(email: EmailStr) -> Optional[User]:
    return await CRUDBase(User).get(email)


async def get_all_users_in_db() -> Optional[CreateOut]:
    return await CRUDBase(User).get_all()


async def create_user_in_db(user: UserCreate) -> CreateOut:
    user.password = get_hashed_password(user.password)

    new_user = await CRUDBase(User).create(user)
    return new_user


async def update_user_in_db(email: EmailStr, details: UserUpdate) -> UpdateOut:
    if details.hashed_password is not None:
        details.hashed_password = get_hashed_password(details.hashed_password)

    updated_user = await CRUDBase(User).update(email, details)
    return updated_user


async def delete_user_in_db(email: EmailStr) -> DeleteOut:
    deleted_user = await CRUDBase(User).delete(email)
    return deleted_user
