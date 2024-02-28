import random
import string
import asyncio

from src.users.services import create_user_in_db

from src.users.schemas import UserCreate


def random_lower_string(length: int) -> str:
    return "".join(random.choices(string.ascii_lowercase, k=length))


def random_email() -> str:
    return f"{random_lower_string(10)}@{random_lower_string(10)}.com"


def create_random_user(is_random=True) -> UserCreate:
    if is_random:
        email = random_email()
    else:
        email = "user@example.com"

    password = random_lower_string(5)
    new_user = UserCreate(email=email, password=password)

    return new_user


async def create_several_users(length: int):
    await asyncio.gather(
        *[create_user_in_db(create_random_user()) for _ in range(length)]
    )


async def create_single_user() -> UserCreate:
    user = create_random_user()
    await create_user_in_db(user.model_copy())

    return user
