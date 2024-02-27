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

from src.users.crud_user import user


async def get_user_by_email(email: EmailStr) -> Optional[User]:
    return await user.get(key="email", value=email)


async def get_all_users_in_db() -> Optional[CreateOut]:
    return await user.get_all()


async def create_user_in_db(create_user: UserCreate) -> CreateOut:
    create_user.hashed_password = get_hashed_password(create_user.hashed_password)

    new_user = await user.create(key="email", value=user.email, schema=create_user)
    return new_user


async def update_user_in_db(email: EmailStr, details: UserUpdate) -> UpdateOut:
    if details.hashed_password is not None:
        details.hashed_password = get_hashed_password(details.hashed_password)

    updated_user = await user.update(key="email", value=email, schema=details)
    return updated_user


async def delete_user_in_db(email: EmailStr) -> DeleteOut:
    deleted_user = await user.delete(key="email", value=email)
    return deleted_user
