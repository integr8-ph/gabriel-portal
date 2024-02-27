from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import EmailStr

from src.auth.dependencies import (
    authenticate_user,
    create_access_token,
    get_current_active_superuser,
    get_current_active_user,
)

from src.auth.exceptions import InvalidUserOrPass
from src.auth.schemas import Token
from src.config import get_settings
from src.users.dependencies import SuperUserDep
from src.users.schemas import (
    DeleteOut,
    CreateOut,
    UpdateOut,
    UserCreate,
    UserUpdate,
)
from src.users.services import (
    create_user_in_db,
    delete_user_in_db,
    get_all_users_in_db,
    get_user_by_email,
    update_user_in_db,
)

router = APIRouter()


@router.post("/login/access-token", include_in_schema=False)
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()]
) -> Token:
    user = await authenticate_user(form_data.username, form_data.password)

    if not user:
        raise InvalidUserOrPass()

    access_token_expires = get_settings().ACCESS_EXPIRE_TOKEN

    access_token = await create_access_token(user.email, access_token_expires)

    return Token(access_token=access_token, token_type="bearer")


@router.post("/user", dependencies=[SuperUserDep])
async def create_user(user: UserCreate) -> CreateOut:
    new_user = await create_user_in_db(user=user)
    return new_user


@router.get("/users", dependencies=[SuperUserDep])
async def get_all_users() -> list[CreateOut]:
    return await get_all_users_in_db()


@router.get("/user/{email}", dependencies=[SuperUserDep])
async def get_user(email: EmailStr) -> CreateOut:
    user = await get_user_by_email(email)
    return user


@router.put("/user/{email}", dependencies=[SuperUserDep])
async def update_user(
    email: EmailStr, to_update: Annotated[UserUpdate, Depends()]
) -> UpdateOut:
    updated_user = await update_user_in_db(email, to_update)
    return updated_user


@router.delete("/user/{email}", dependencies=[SuperUserDep])
async def delete_user(email: EmailStr) -> DeleteOut:
    deleted_user = await delete_user_in_db(email)
    return deleted_user


@router.get("/me", include_in_schema=False)
async def dashboard(user: CreateOut = Depends(get_current_active_user)):
    return user


@router.get("/admin", include_in_schema=False)
async def admin(user: Annotated[CreateOut, Depends(get_current_active_superuser)]):
    return user
