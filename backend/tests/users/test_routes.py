import pytest
from fastapi.encoders import jsonable_encoder
from httpx import AsyncClient

from tests.utils.utils import (
    create_random_user,
    create_several_users,
    create_single_user,
    random_lower_string,
)
from src.auth.services import verify_password


@pytest.mark.asyncio
async def test_login_for_access_token(client: AsyncClient) -> None:
    user = create_random_user()

    # CHECK CREDENTIALS
    await client.post("/user", json=jsonable_encoder(user))
    form_data = {"username": user.email, "password": user.password}

    response = await client.post("/login/access-token", data=form_data)
    assert response.status_code == 200
    assert "access_token" in response.json()
    assert "token_type" in response.json()

    # INVALID CREDENTIALS
    form_data["username"] = "random@example.com"
    response = await client.post("login/access-token", data=form_data)
    assert response.status_code == 401

    # INVALID DATA
    response = await client.post("login/access-token", data={})
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_create_user(client: AsyncClient) -> None:
    new_user = create_random_user()

    # CREATE USER
    response = await client.post("/user", json=jsonable_encoder(new_user))

    assert response.status_code == 200
    response_data = response.json()

    assert response_data["email"] == new_user.email
    assert verify_password(new_user.password, response_data["hashed_password"])
    assert response_data["is_superuser"] is True
    assert response_data["is_active"] is True
    assert "created_at" in response_data

    # CHECK EXISTING USER
    response = await client.post("/user", json=jsonable_encoder(new_user))
    assert response.status_code == 409

    # INVALID DATA
    response = await client.post("/user", json={})
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_get_all_users(client: AsyncClient) -> None:
    # CREATE NUMBER OF USERS
    await create_several_users(3)

    # GET ALL USERS
    response = await client.get("/users")

    assert response.status_code == 200
    response_data = response.json()

    assert isinstance(response_data, list)
    assert len(response_data) == 3


@pytest.mark.asyncio
async def test_get_user(client: AsyncClient) -> None:
    user = await create_single_user()

    # CHECK USER
    response = await client.get(f"/user/{user.email}")

    assert response.status_code == 200
    response_data = response.json()

    assert response_data["email"] == user.email
    assert verify_password(user.password, response_data["hashed_password"])
    assert response_data["is_superuser"] is True
    assert response_data["is_active"] is True
    assert "created_at" in response_data

    # CHECK NON-EXISTING USER
    response = await client.get("/user/abcd@efg.com")
    assert response.status_code == 404

    # INVALID EMAIL
    response = await client.get("/user/abcd")
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_update_user(client: AsyncClient) -> None:
    user = await create_single_user()

    # UPDATE USER
    to_change = {
        "password": random_lower_string(5),
        "is_active": False,
        "is_superuser": False,
    }

    response = await client.put(f"/user/{user.email}", params=to_change)
    assert response.status_code == 200

    response_data = response.json()

    assert response_data["email"] == user.email
    assert verify_password(to_change["password"], response_data["hashed_password"])
    assert response_data["is_superuser"] is to_change["is_superuser"]
    assert response_data["is_active"] is to_change["is_active"]
    assert "updated_at" in response_data

    # CHECK IF USER IS REALLY UPDATED
    response = await client.get(f"user/{user.email}")
    assert response.status_code == 200

    response_data = response.json()

    assert verify_password(to_change["password"], response_data["hashed_password"])
    assert response_data["is_superuser"] is to_change["is_superuser"]
    assert response_data["is_active"] is to_change["is_active"]

    # UPDATE NON-EXISTING USER
    response = await client.put("/user/abcd@efg.com")
    assert response.status_code == 404

    # INVALID EMAIL
    response = await client.get("/user/abcd")
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_delete_user(client: AsyncClient) -> None:
    user = await create_single_user()

    # DELETE USER
    response = await client.delete(f"/user/{user.email}")
    assert response.status_code == 200

    response_data = response.json()

    assert response_data["email"] == user.email
    assert verify_password(user.password, response_data["hashed_password"])
    assert response_data["is_superuser"] is True
    assert response_data["is_active"] is True
    assert "deleted_at" in response_data

    # CHECK IF USER IS REALLY DELETED
    response = await client.get(f"/user/{user.email}")
    assert response.status_code == 404

    # DELETE NON-EXISTING USER
    response = await client.delete("/user/abcd@efg.com")
    assert response.status_code == 404

    # INVALID EMAIl
    response = await client.delete("/user/abcd")
    assert response.status_code == 422
