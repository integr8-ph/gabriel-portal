from typing import Generic, Type, TypeVar, Optional, Any

from beanie import Document
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel

from src.exceptions import Conflict, NotFound

ModelType = TypeVar("ModelType", bound=Document)


class CRUDBase(Generic[ModelType]):
    def __init__(self, model: Type[ModelType]):
        self.model = model

    async def get(self, key: str, value: Any) -> Optional[ModelType]:
        doc = await self.model.find_one({key: value})
        if not doc:
            raise NotFound()

        return doc

    async def get_all(self) -> Optional[list[ModelType]]:
        return await self.model.find_all().to_list()

    async def create(
        self, key: str, value: Any, schema: BaseModel
    ) -> Optional[ModelType]:
        if await self.model.find_one({key: value}):
            raise Conflict()

        created_doc = await self.model(**schema.model_dump()).insert()
        return jsonable_encoder(created_doc)

    async def update(
        self, key: str, value: Any, schema: BaseModel
    ) -> Optional[ModelType]:
        doc = await self.get(key=key, value=value)

        updated_doc = await doc.set(
            {**schema.model_dump(exclude_none=True, exclude_unset=True)}
        )
        return jsonable_encoder(updated_doc)

    async def delete(self, key: str, value: Any) -> Optional[ModelType]:
        deleted_doc = await self.get(key=key, value=value)

        await deleted_doc.delete()
        return jsonable_encoder(deleted_doc)
