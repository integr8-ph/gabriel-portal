from pydantic import BaseModel, EmailStr, validator
from datetime import datetime


class UserCreate(BaseModel):
    email: EmailStr
    password: str
    is_superuser: bool = True


class UserOut(BaseModel):
    email: EmailStr
    created_at: datetime
