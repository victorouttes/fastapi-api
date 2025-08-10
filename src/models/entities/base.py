from typing import Any, Generic, TypeVar

from pydantic import BaseModel
from sqlmodel import SQLModel

T = TypeVar("T", bound=SQLModel)

class EntityList(BaseModel, Generic[T]):
    items: list[T]
    total: int
    page: int
    page_size: int
    pages: int

class DeletedMessage(BaseModel):
    message: str
