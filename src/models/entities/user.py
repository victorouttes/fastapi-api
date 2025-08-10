from datetime import datetime

from sqlalchemy import Column, DateTime
from sqlmodel import SQLModel, Field
from zoneinfo import ZoneInfo

class User(SQLModel, table=True):
    id: int = Field(primary_key=True)
    username: str = Field(unique=True, index=True)
    email: str = Field(unique=True, index=True)
    password: str
    created_at: datetime = Field(
        sa_column=Column(DateTime(timezone=True), nullable=False),
        default_factory=lambda: datetime.now(ZoneInfo('UTC'))
    )
    updated_at: datetime = Field(
        sa_column=Column(DateTime(timezone=True), nullable=False),
        default_factory=lambda: datetime.now(ZoneInfo('UTC'))
    )

class UserCreate(SQLModel):
    username: str
    email: str
    password: str

class UserUpdate(SQLModel):
    username: str | None = None
    email: str | None = None
    password: str | None = None

class UserPublic(SQLModel):
    id: int
    username: str
    email: str
    created_at: datetime
    updated_at: datetime
