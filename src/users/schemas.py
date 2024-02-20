from typing import Annotated

from pydantic import BaseModel, EmailStr, Field
from datetime import datetime


class UserCreate(BaseModel):
    email: EmailStr
    password: str
    is_superuser: bool = True


class UserUpdate(BaseModel):
    hashed_password: Annotated[str | None, Field(alias="password")] = None
    is_active: bool | None = None
    is_superuser: bool | None = None


class UserOut(BaseModel):
    email: EmailStr
    created_at: datetime


class BaseCompleteUser(BaseModel):
    email: EmailStr
    hashed_password: str
    is_active: bool = True
    is_superuser: bool = True


class CompleteUserOut(BaseCompleteUser):
    created_at: datetime


class CompleteUserUpdateOut(BaseCompleteUser):
    updated_at: Annotated[datetime, Field(default_factory=datetime.utcnow)]


class CompleteUserDeleteOut(BaseCompleteUser):
    deleted_at: Annotated[datetime, Field(default_factory=datetime.utcnow)]
