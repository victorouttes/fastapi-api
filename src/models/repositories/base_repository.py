from math import ceil
from typing import Type, TypeVar, Generic, Optional, Any, get_args, get_origin

from sqlalchemy import func
from sqlmodel import SQLModel, select

from src.models.settings.db_connection_handler import db_connection_handler

T = TypeVar("T", bound=SQLModel)


class BaseRepository(Generic[T]):
    model_class: Type[T]

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        # Tenta inferir T do parâmetro genérico da subclasse
        for base in getattr(cls, "__orig_bases__", []):
            origin = get_origin(base)
            if origin is BaseRepository:
                args = get_args(base)
                if args:
                    cls.model_class = args[0]  # type: ignore[assignment]

    def __init__(self):
        self._session_factory = db_connection_handler.get_session()

    async def create(self, **data: Any) -> T:
        obj = self.model_class(**data)
        async with self._session_factory() as session:
            session.add(obj)
            await session.commit()
            await session.refresh(obj)
            return obj

    async def get_by_id(self, id: int) -> Optional[T]:
        async with self._session_factory() as session:
            stmt = select(self.model_class).where(self.model_class.id == id)
            result = await session.execute(stmt)
            return result.scalar_one_or_none()

    async def get_paginated(self, page: int = 1, page_size: int = 10) -> dict[str, Any]:
        if page < 1:
            raise ValueError("page must be >= 1")
        if page_size < 1:
            raise ValueError("page_size must be >= 1")

        async with self._session_factory() as session:
            total_res = await session.execute(
                select(func.count()).select_from(self.model_class)
            )
            total = total_res.scalar_one() or 0

            # page items
            stmt = (
                select(self.model_class)
                .offset((page - 1) * page_size)
                .limit(page_size)
            )
            result = await session.execute(stmt)
            items = result.scalars().all()

            pages = ceil(total / page_size) if total else 0

            return {
                "items": items,
                "total": total,
                "page": page,
                "page_size": page_size,
                "pages": pages,
            }


    async def delete_by_id(self, id: int) -> bool:
        async with self._session_factory() as session:
            stmt = select(self.model_class).where(self.model_class.id == id)
            result = await session.execute(stmt)
            obj = result.scalar_one_or_none()
            if not obj:
                return False
            await session.delete(obj)
            await session.commit()
            return True

    async def update_by_id(self, id: int, **data: Any) -> Optional[T]:
        async with self._session_factory() as session:
            stmt = select(self.model_class).where(self.model_class.id == id)
            result = await session.execute(stmt)
            obj = result.scalar_one_or_none()
            if not obj:
                return None
            for k, v in data.items():
                if hasattr(obj, k):
                    setattr(obj, k, v)
            await session.commit()
            await session.refresh(obj)
            return obj
