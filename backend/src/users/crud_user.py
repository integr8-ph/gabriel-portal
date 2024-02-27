from typing import Optional, Any, TypeVar

from beanie import Document

from src.users.models import User
from src.users.exceptions import UserNotFound
from src.crud import CRUDBase

ModelType = TypeVar("ModelType", bound=Document)


class CRUDUser(CRUDBase):
    async def get(self, key: str, value: Any) -> Optional[ModelType]:
        doc = await self.model.find_one({key: value})
        if not doc:
            raise UserNotFound()

        return doc


user = CRUDUser(User)
