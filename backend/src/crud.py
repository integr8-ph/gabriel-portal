from typing import Generic, Type, TypeVar, Optional, Any

from beanie import Document
from pydantic import BaseModel

ModelType = TypeVar("ModelType", bound=Document)


class CRUDBase(Generic[ModelType]):
    def __init__(self, model: Type[ModelType]):
        self.model = model

    async def get(self, key: str, value: Any) -> Optional[ModelType]:
        return await self.model.find_one({key: value})

    async def get_all(self) -> Optional[list[ModelType]]:
        return await self.model.find_all().to_list()

    async def create(self, schema: BaseModel) -> Optional[ModelType]:
        return await self.model(**schema.model_dump()).insert()

    async def update(self, details: BaseModel, doc: Document) -> Optional[ModelType]:
        return await doc.set(
            {**details.model_dump(exclude_none=True, exclude_unset=True)}
        )

    async def delete(self, doc: Document) -> Optional[ModelType]:
        await doc.delete()
