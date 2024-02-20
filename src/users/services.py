from typing import Optional

from fastapi.encoders import jsonable_encoder
from pydantic import EmailStr
from src.auth.services import get_hashed_password, verify_password

from src.users.models import User
from src.users.schemas import UserCreate


async def get_user_by_email(email: EmailStr) -> Optional[User]:
    return await User.find_one(User.email == email)


async def create_user(user: UserCreate) -> User:
    user.password = get_hashed_password(user.password)
    new_user = await User(
        email=user.email, hashed_password=user.password, is_superuser=user.is_superuser
    ).insert()

    json_encode_user = jsonable_encoder(new_user)

    return json_encode_user
