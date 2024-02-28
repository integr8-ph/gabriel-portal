from typing import Optional

from fastapi.encoders import jsonable_encoder
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


async def get_user_by_email(email: EmailStr) -> Optional[User]:
    return await User.find_one(User.email == email)


async def get_all_users_in_db() -> Optional[CreateOut]:
    return await User.find().to_list()


async def update_user_in_db(user: User, details: UserUpdate) -> UpdateOut:
    to_update = {**details.model_dump(exclude_none=True)}

    password = to_update.get("hashed_password", None)
    if password:
        to_update["hashed_password"] = get_hashed_password(password)

    updated_user = await user.set(to_update)

    json_encode_updated_user = jsonable_encoder(updated_user)

    return json_encode_updated_user


async def delete_user_in_db(user: User) -> DeleteOut:
    await user.delete()

    json_encode_deleted_user = jsonable_encoder(user)

    return json_encode_deleted_user


async def create_user_in_db(user: UserCreate) -> CreateOut:
    user.password = get_hashed_password(user.password)
    new_user = await User(
        email=user.email, hashed_password=user.password, is_superuser=user.is_superuser
    ).insert()

    json_encode_created_user = jsonable_encoder(new_user)

    return json_encode_created_user
