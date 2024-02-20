from beanie import Document, Indexed
from datetime import datetime
from pydantic import Field, EmailStr


class User(Document):
    email: Indexed(EmailStr, unique=True)  # type: ignore
    hashed_password: str
    is_active: bool = True
    is_superuser: bool = True
    created_at: datetime = Field(default_factory=datetime.utcnow)
