from typing import Generic, TypeVar, Any, get_origin, get_args, Type

from sqlmodel import SQLModel

from src.models.repositories.base_repository import BaseRepository

T = TypeVar("T", bound=SQLModel)
R = TypeVar("R", bound=BaseRepository[Any])

class BaseController(Generic[T, R]):
    repository_class: Type[R]

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        # Tenta inferir R do parâmetro genérico da subclasse
        for base in getattr(cls, "__orig_bases__", []):
            origin = get_origin(base)
            if origin is BaseController:
                args = get_args(base)
                if len(args) >= 2:
                    repo_arg = args[1]
                    if isinstance(repo_arg, type):
                        cls.repository_class = repo_arg  # type: ignore[assignment]
                break

    def __init__(self):
        self.__repository: R = self.repository_class()

    async def get_paginated(self, page: int = 1, page_size: int = 10) -> dict[str, Any]:
        return await self.__repository.get_paginated(page, page_size)

    async def get_by_id(self, id: int) -> T:
        return await self.__repository.get_by_id(id)

    async def create(self, **data: Any) -> T:
        return await self.__repository.create(**data)

    async def update(self, id: int, **data: Any) -> T:
        return await self.__repository.update_by_id(id, **data)

    async def delete(self, id: int) -> bool:
        return await self.__repository.delete_by_id(id)
