from typing import Annotated

from pydantic import BaseModel, EmailStr, Field
from datetime import datetime


class UserCreate(BaseModel):
    email: EmailStr
    hashed_password: Annotated[str, Field(alias="password")]
    is_superuser: bool = True


class UserUpdate(BaseModel):
    hashed_password: Annotated[str | None, Field(alias="password")] = None
    is_active: bool | None = None
    is_superuser: bool | None = None


class BaseOut(BaseModel):
    email: EmailStr
    hashed_password: str
    is_active: bool
    is_superuser: bool


class CreateOut(BaseOut):
    created_at: datetime


class UpdateOut(BaseOut):
    updated_at: Annotated[datetime, Field(default_factory=datetime.utcnow)]


class DeleteOut(BaseOut):
    deleted_at: Annotated[datetime, Field(default_factory=datetime.utcnow)]
