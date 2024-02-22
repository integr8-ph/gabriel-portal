import pytest
import pytest_asyncio

from async_asgi_testclient import TestClient
from src.auth.dependencies import get_current_active_superuser
from src.auth.services import verify_password

from src.main import app
from tests.users.data import (
    CreateUser,
    DeleteUser,
    GetAllUsers,
    GetUser,
    OAuth2,
    UpdateUser,
)

HOST = "127.0.0.1"
PORT = "8000"


@pytest_asyncio.fixture
async def client():
    scope = {"client": (HOST, PORT)}

    async with TestClient(application=app, scope=scope) as client:
        yield client


@pytest_asyncio.fixture
async def skip_authentication_client():
    scope = {"client": (HOST, PORT)}

    async def skip():
        pass

    app.dependency_overrides[get_current_active_superuser] = skip

    async with TestClient(application=app, scope=scope) as client:
        yield client


@pytest.mark.asyncio
@pytest.mark.parametrize("params", OAuth2.PAYLOADS)
async def test_login_for_access_token(client: TestClient, params: OAuth2):
    username, password, expected_status_code = params

    test_data = {"username": username, "password": password}

    response = await client.post(
        "/login/access-token",
        form=test_data,
    )

    assert response.status_code == expected_status_code

    if response.status_code == 200:
        response_data = response.json()

        assert "access_token" in response_data
        assert "token_type" in response_data


@pytest.mark.asyncio
@pytest.mark.parametrize("params", CreateUser.PAYLOADS)
async def test_create_user(skip_authentication_client: TestClient, params: CreateUser):
    email, password, is_superuser, expected_status_code = params

    test_data = {"email": email, "password": password, "is_superuser": is_superuser}

    response = await skip_authentication_client.post("/user", json=test_data)

    assert response.status_code == expected_status_code

    if response.status_code == 200:
        response_data = response.json()

        assert CreateUser.SUCCESSFUL_RESPONSE.items() <= response_data.items()
        assert verify_password("asd", response_data["hashed_password"])
        assert "created_at" in response_data


@pytest.mark.asyncio
@pytest.mark.parametrize("params", UpdateUser.PAYLOADS)
async def test_update_user(skip_authentication_client: TestClient, params: UpdateUser):
    (
        email,
        password,
        is_active,
        is_superuser,
        successful_response,
        expected_status_code,
    ) = params

    response = await skip_authentication_client.put(
        f"/user/{email}?password={password}&is_active={is_active}&is_superuser={is_superuser}"  # noqa
    )

    assert response.status_code == expected_status_code

    if response.status_code == 200:
        response_data = response.json()

        assert successful_response.items() <= response_data.items()
        assert verify_password("qwe", response_data["hashed_password"])
        assert "updated_at" in response_data


@pytest.mark.asyncio
@pytest.mark.parametrize("params", DeleteUser.PAYLOADS)
async def test_delete_user(skip_authentication_client: TestClient, params: DeleteUser):
    email, successful_response, expected_status_code = params

    response = await skip_authentication_client.delete(f"/user/{email}")

    assert response.status_code == expected_status_code

    if response.status_code == 200:
        response_data = response.json()

        assert successful_response.items() <= response_data.items()
        assert verify_password("qwe", response_data["hashed_password"])
        assert "deleted_at" in response_data


@pytest.mark.asyncio
async def test_get_all_users(skip_authentication_client: TestClient):
    response = await skip_authentication_client.get("/users")

    assert response.status_code == 200

    response_data = response.json()

    assert response_data == GetAllUsers.SUCCESSFUL_RESPONSE


@pytest.mark.asyncio
@pytest.mark.parametrize("params", GetUser.PAYLOADS)
async def test_get_user(skip_authentication_client: TestClient, params: GetUser):
    email, successful_response, expected_status_code = params

    response = await skip_authentication_client.get(f"/user/{email}")

    assert response.status_code == expected_status_code

    if response.status_code == 200:
        assert response.json() == successful_response
