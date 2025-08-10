from http import HTTPStatus
from math import ceil
from typing import Type, TypeVar, Generic, Optional, get_args, get_origin

from fastapi import HTTPException
from sqlalchemy import func
from sqlalchemy.exc import IntegrityError
from sqlmodel import SQLModel, select

from src.models.entities.base import EntityList
from src.models.settings.db_connection_handler import db_connection_handler

Model = TypeVar("Model", bound=SQLModel)
SchemaCreate = TypeVar("SchemaCreate", bound=SQLModel)
SchemaUpdate = TypeVar("SchemaUpdate", bound=SQLModel)

class BaseRepository(Generic[Model, SchemaCreate, SchemaUpdate]):
    model_class: Type[Model]
    create_class: Type[SchemaCreate]
    update_class: Type[SchemaUpdate]

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        for base in getattr(cls, "__orig_bases__", []):
            origin = get_origin(base)
            if origin is BaseRepository:
                args = get_args(base)
                if args:
                    cls.model_class = args[0]  # type: ignore[assignment]
                    cls.create_class = args[1]  # type: ignore[assignment]
                    cls.update_class = args[2]  # type: ignore[assignment]

    def __init__(self):
        self._session_factory = db_connection_handler.get_session()

    async def create(self, data: SchemaCreate) -> Model:
        data_dict = data.model_dump(exclude_unset=True)
        obj = self.model_class(**data_dict)
        async with self._session_factory() as session:
            try:
                session.add(obj)
                await session.commit()
                await session.refresh(obj)
                return obj
            except IntegrityError as e:
                await session.rollback()
                orig = getattr(e, "orig", None)
                detail = getattr(orig, "detail", None) or str(orig)
                raise HTTPException(status_code=HTTPStatus.CONFLICT, detail=detail)

    async def get_by_id(self, id: int) -> Optional[Model]:
        async with self._session_factory() as session:
            stmt = select(self.model_class).where(self.model_class.id == id)
            result = await session.execute(stmt)
            return result.scalar_one_or_none()

    async def get_paginated(self, page: int = 1, page_size: int = 10) -> EntityList[Model]:
        if page < 1:
            raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail="page must be >= 1")
        if page_size < 1:
            raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail="page_size must be >= 1")

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

            return EntityList(items=items, total=total, page=page, page_size=page_size, pages=pages)


    async def delete_by_id(self, id: int) -> bool:
        async with self._session_factory() as session:
            stmt = select(self.model_class).where(self.model_class.id == id)
            result = await session.execute(stmt)
            obj = result.scalar_one_or_none()
            if not obj:
                raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Identifier not found")
            await session.delete(obj)
            await session.commit()
            return True

    async def update_by_id(self, id: int, data: SchemaUpdate) -> Optional[Model]:
        async with self._session_factory() as session:
            data_dict = data.model_dump(exclude_unset=True)
            stmt = select(self.model_class).where(self.model_class.id == id)
            result = await session.execute(stmt)
            obj = result.scalar_one_or_none()
            if not obj:
                raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Identifier not found")
            for k, v in data_dict.items():
                if hasattr(obj, k):
                    setattr(obj, k, v)
            try:
                await session.commit()
                await session.refresh(obj)
                return obj
            except IntegrityError as e:
                await session.rollback()
                orig = getattr(e, "orig", None)
                detail = getattr(orig, "detail", None) or str(orig)
                raise HTTPException(status_code=HTTPStatus.CONFLICT, detail=detail)
