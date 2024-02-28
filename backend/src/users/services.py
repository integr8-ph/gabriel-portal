from typing import Optional
from fastapi.encoders import jsonable_encoder

from pydantic import EmailStr
from src.exceptions import Conflict
from src.users.exceptions import UserNotFound
from src.auth.services import get_hashed_password

from src.users.models import User
from src.users.schemas import (
    DeleteOut,
    CreateOut,
    UpdateOut,
    UserCreate,
    UserUpdate,
)

from src.users.crud_user import user_crud


async def check_user_exists(email: EmailStr) -> Optional[User]:
    user = await get_user_by_email(email=email)

    if not user:
        raise UserNotFound()

    return user


async def get_user_by_email(email: EmailStr) -> Optional[User]:
    return await user_crud.get(key="email", value=email)


async def get_all_users_in_db() -> Optional[CreateOut]:
    return await user_crud.get_all()


async def create_user_in_db(create_user: UserCreate) -> CreateOut:
    user = await get_user_by_email(email=create_user.email)

    if user:
        raise Conflict()

    create_user.hashed_password = get_hashed_password(create_user.hashed_password)

    new_user = await user_crud.create(schema=create_user)
    return jsonable_encoder(new_user)


async def update_user_in_db(email: EmailStr, details: UserUpdate) -> UpdateOut:
    user = await check_user_exists(email=email)

    if details.hashed_password is not None:
        details.hashed_password = get_hashed_password(details.hashed_password)

    updated_user = await user_crud.update(details=details, doc=user)
    return jsonable_encoder(updated_user)


async def delete_user_in_db(email: EmailStr) -> DeleteOut:
    user = await check_user_exists(email=email)

    await user_crud.delete(doc=user)
    return jsonable_encoder(user)
