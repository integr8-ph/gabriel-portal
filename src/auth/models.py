from beanie import Document


class UserCreate(Document):
    username: str
    password: str
