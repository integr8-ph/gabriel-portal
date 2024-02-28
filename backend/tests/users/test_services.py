import pytest

from src.auth.services import verify_password
from src.users.schemas import UserCreate, UserUpdate
from src.users.models import User
from src.users.services import (
    create_user_in_db,
    delete_user_in_db,
    get_all_users_in_db,
    get_user_by_email,
    update_user_in_db,
)
from tests.utils.utils import (
    create_several_users,
    create_single_user,
    random_email,
    random_lower_string,
)


@pytest.mark.asyncio
async def test_get_user_by_email() -> None:
    user = await create_single_user()

    output = await get_user_by_email(user.email)
    assert isinstance(output, User)
    assert output.email == user.email

    output = await get_user_by_email("abcd@efg.com")
    assert output is None


@pytest.mark.asyncio
async def test_get_all_users_in_db() -> None:
    output = await get_all_users_in_db()
    assert output == []

    await create_several_users(3)

    output = await get_all_users_in_db()
    assert isinstance(output[0], User)
    assert len(output) == 3


@pytest.mark.asyncio
async def test_update_user_in_db() -> None:
    user = await create_single_user()
    to_update = UserUpdate(password=random_lower_string(5), is_active=False)

    to_update_user = await get_user_by_email(user.email)
    assert isinstance(to_update_user, User)
    assert to_update_user.email == user.email

    updated_user = await update_user_in_db(to_update_user, to_update.model_copy())
    assert isinstance(updated_user, dict)
    assert verify_password(to_update.hashed_password, updated_user["hashed_password"])
    assert updated_user["is_superuser"] is True
    assert updated_user["is_active"] is False
    assert "_id" in updated_user
    assert "created_at" in updated_user


@pytest.mark.asyncio
async def test_delete_user_in_db() -> None:
    user = await create_single_user()

    to_delete_user = await get_user_by_email(user.email)
    assert isinstance(to_delete_user, User)
    assert to_delete_user.email == user.email

    deleted_user = await delete_user_in_db(to_delete_user)
    assert isinstance(deleted_user, dict)
    assert verify_password(user.password, deleted_user["hashed_password"])
    assert deleted_user["is_superuser"] is True
    assert deleted_user["is_active"] is True
    assert "_id" in deleted_user
    assert "created_at" in deleted_user


@pytest.mark.asyncio
async def test_create_user_in_db() -> None:
    to_create_user = UserCreate(
        email=random_email(), password=random_lower_string(5), is_superuser=True
    )

    created_user = await create_user_in_db(to_create_user.model_copy())
    assert isinstance(created_user, dict)
    assert verify_password(to_create_user.password, created_user["hashed_password"])
    assert created_user["is_superuser"] is True
    assert created_user["is_active"] is True
    assert "_id" in created_user
    assert "created_at" in created_user
