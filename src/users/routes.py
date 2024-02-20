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
from src.users.exceptions import UserNotFound
from src.users.schemas import (
    CompleteUserDeleteOut,
    CompleteUserOut,
    CompleteUserUpdateOut,
    UserCreate,
    UserOut,
    UserUpdate,
)
from src.users.services import (
    create_user,
    delete_user_in_db,
    get_all_users_in_db,
    get_user_by_email,
    update_user_in_db,
)
from src.exceptions import Conflict

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


@router.post("/signup", dependencies=[Depends(get_current_active_superuser)])
async def signup(user: UserCreate) -> UserOut:
    new_user = await get_user_by_email(user.email)

    if new_user:
        raise Conflict()

    new_user = await create_user(user=user)

    return new_user


SuperUserDep = Depends(get_current_active_superuser)


@router.get("/users", dependencies=[SuperUserDep])
async def get_all_users() -> list[CompleteUserOut]:
    return await get_all_users_in_db()


@router.get("/user/{email}", dependencies=[SuperUserDep])
async def get_user(email: EmailStr) -> CompleteUserOut:
    user = await get_user_by_email(email)

    if not user:
        raise UserNotFound()

    return user


@router.put("/user/{email}", dependencies=[SuperUserDep])
async def update_user(
    email: EmailStr, to_update: Annotated[UserUpdate, Depends()]
) -> CompleteUserUpdateOut:
    user = await get_user_by_email(email)

    if not user:
        raise UserNotFound()

    updated_user = await update_user_in_db(user, to_update)

    return updated_user


@router.delete("/user/{email}", dependencies=[SuperUserDep])
async def delete_user(email: EmailStr) -> CompleteUserDeleteOut:
    user = await get_user_by_email(email)

    if not user:
        raise UserNotFound()

    deleted_user = await delete_user_in_db(user)

    return deleted_user


@router.get("/me", include_in_schema=False)
async def dashboard(user: UserOut = Depends(get_current_active_user)):
    return user


@router.get("/admin", include_in_schema=False)
async def admin(user: Annotated[UserOut, Depends(get_current_active_superuser)]):
    return user
