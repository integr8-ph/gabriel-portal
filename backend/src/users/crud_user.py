from typing import TypeVar

from beanie import Document

from src.users.models import User
from src.crud import CRUDBase

ModelType = TypeVar("ModelType", bound=Document)


class CRUDUser(CRUDBase):
    pass


user_crud = CRUDUser(User)
