from typing import Generic, TypeVar, get_origin, get_args, Type

from sqlmodel import SQLModel

from src.models.entities.base import EntityList
from src.models.repositories.base_repository import BaseRepository

Model = TypeVar("Model", bound=SQLModel)
SchemaCreate = TypeVar("SchemaCreate", bound=SQLModel)
SchemaUpdate = TypeVar("SchemaUpdate", bound=SQLModel)
Repository = TypeVar("Repository", bound=BaseRepository)

class BaseController(Generic[Model, SchemaCreate, SchemaUpdate, Repository]):
    model_class: Type[Model]
    create_class: Type[SchemaCreate]
    update_class: Type[SchemaUpdate]
    repository_class: Type[Repository]

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        for base in getattr(cls, "__orig_bases__", []):
            origin = get_origin(base)
            if origin is BaseController:
                args = get_args(base)
                if args:
                    cls.model_class = args[0]  # type: ignore[assignment]
                    cls.create_class = args[1]  # type: ignore[assignment]
                    cls.update_class = args[2]  # type: ignore[assignment]
                    cls.repository_class = args[3]  # type: ignore[assignment]

    def __init__(self):
        self.__repository: Repository = self.repository_class()

    async def get_paginated(self, page: int = 1, page_size: int = 10) -> EntityList[Model]:
        return await self.__repository.get_paginated(page, page_size)

    async def get_by_id(self, id: int) -> Model:
        return await self.__repository.get_by_id(id)

    async def create(self, data: SchemaCreate) -> Model:
        return await self.__repository.create(data)

    async def update(self, id: int, data: SchemaUpdate) -> Model:
        return await self.__repository.update_by_id(id, data)

    async def delete(self, id: int) -> bool:
        return await self.__repository.delete_by_id(id)
