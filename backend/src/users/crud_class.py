from typing import Any, Generic, Optional, Type, TypeVar  # noqa
from bson import ObjectId  # noqa
from fastapi.encoders import jsonable_encoder  # noqa

from beanie import Document  # noqa
from pydantic import BaseModel, EmailStr

from src.exceptions import Conflict
from src.users.exceptions import UserNotFound
from src.auth.services import get_hashed_password  # noqa


# ModelType = TypeVar("ModelType", bound=Any)
# CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
# UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


# class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
#     def __init__(self, model: Type[ModelType]):
#         self.model = model

#     async def get(self, id: str) -> Optional[ModelType]:
#         return await self.model.find_one({"_id": ObjectId(id)})

#     async def update(self, id: str, scheme: Any) -> Optional[ModelType]:
#         await self.model.find_one({"_id": ObjectId(id)}).update(
#             {"$set": scheme.model_dump(exclude_unset=True)}
#         )
#         updated_doc = await self.get(id=id, model=self.model)
#         return updated_doc

ModelType = TypeVar("ModelType", bound=Document)


class CRUDBase(Generic[ModelType]):
    def __init__(self, model: Type[ModelType]):
        self.model = model

    async def get(self, email: EmailStr) -> Optional[ModelType]:
        user = await self.model.find_one({"email": email})
        if not user:
            raise UserNotFound()

        return user

    async def get_all(self) -> Optional[list[ModelType]]:
        return await self.model.find_all().to_list()

    async def create(self, schema: BaseModel) -> Optional[ModelType]:
        if await self.model.find_one({"email": schema.email}):
            raise Conflict()

        created_user = await self.model(
            **schema.model_dump(exclude=["password"]), hashed_password=schema.password
        ).insert()
        return jsonable_encoder(created_user)

    async def update(self, email: EmailStr, schema: BaseModel) -> Optional[ModelType]:
        user = await self.get(email=email)
        updated_user = await user.set({**schema.model_dump(exclude_none=True)})
        return jsonable_encoder(updated_user)

    async def delete(self, email: EmailStr) -> Optional[ModelType]:
        user = await self.get(email=email)
        await user.delete()
        return jsonable_encoder(user)
