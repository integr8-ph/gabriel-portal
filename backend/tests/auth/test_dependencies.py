import time
import pytest
from jose import jwt

from src.auth.exceptions import InactiveUser, NotSuperuser
from src.exceptions import NotAuthenticated
from src.config import get_settings
from src.users.exceptions import UserNotFound
from src.users.models import User
from src.auth.dependencies import (
    authenticate_user,
    authenticate_user_by_email,
    create_access_token,
    get_current_active_superuser,
    get_current_active_user,
    get_current_user,
)
from src.auth.services import get_hashed_password, verify_password
from tests.utils.utils import create_single_user, random_lower_string


@pytest.mark.asyncio
async def test_authenticate_user(clear_test_database) -> None:
    user = await create_single_user()

    # AUTHENTICATE USER
    output = await authenticate_user(user.email, user.password)
    assert isinstance(output, User)
    assert output.email == user.email
    assert verify_password(user.password, output.hashed_password)

    # AUTHENTICATE NON-EXISTING EMAIL
    output = await authenticate_user("abcd@efg.com", user.password)
    assert output is False

    # AUTHENTICATE INVALID PASSWORD
    output = await authenticate_user(user.email, "qwerty")
    assert output is False


@pytest.mark.asyncio
async def test_authenticate_user_by_email(clear_test_database) -> None:
    user = await create_single_user()

    # AUTHENTICATE USER
    output = await authenticate_user_by_email(user.email)
    assert isinstance(output, User)
    assert output.email == user.email

    # AUTHENTICATE NON-EXISTING EMAIL
    with pytest.raises(UserNotFound):
        await authenticate_user_by_email("abcd@efg.com")


@pytest.mark.asyncio
async def test_create_access_token() -> None:
    # EXPIRY TIME: 30 days
    fake_email = "fake@example.com"

    token = await create_access_token(fake_email, 30)
    decoded_payload = jwt.decode(
        token, get_settings().SECRET_KEY, get_settings().ALGORITHM
    )

    assert decoded_payload["sub"] == fake_email
    assert "exp" in decoded_payload

    expiration_time = int(decoded_payload["exp"])
    current_time = int(time.time())

    assert current_time < expiration_time

    # CHECK TOKEN 31 DAYS LATER

    current_time = int(time.time()) + (31 * 86_400)

    assert current_time > expiration_time


@pytest.mark.asyncio
async def test_get_current_user(clear_test_database) -> None:
    user = await create_single_user()

    # CHECK CURRENT USER
    fake_token = await create_access_token(user.email, 30)
    output = await get_current_user(fake_token)
    assert isinstance(output, User)
    assert output.email == user.email

    # CHECK INVALID EMAIL
    fake_token = await create_access_token("fake@example.com", 30)
    with pytest.raises(NotAuthenticated):
        await get_current_user(fake_token)


@pytest.mark.asyncio
async def test_get_current_active_user(clear_test_database) -> None:
    user = User(
        email="fake@exameple.com",
        hashed_password=get_hashed_password(random_lower_string(5)),
    )

    # ACTIVE USER
    output = await get_current_active_user(user)
    assert user.email == output.email
    assert user.is_active is True

    # INACTIVE USER
    user.is_active = False
    with pytest.raises(InactiveUser):
        await get_current_active_user(user)


@pytest.mark.asyncio
async def test_get_current_active_superuser(clear_test_database) -> None:
    user = User(
        email="fake@exameple.com",
        hashed_password=get_hashed_password(random_lower_string(5)),
    )

    # ACTIVE USER
    output = await get_current_active_user(user)
    assert user.email == output.email
    assert user.is_superuser is True

    # INACTIVE USER
    user.is_superuser = False
    with pytest.raises(NotSuperuser):
        await get_current_active_superuser(user)
