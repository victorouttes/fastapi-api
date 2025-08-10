from datetime import datetime

from sqlalchemy import Column, DateTime, event, inspect
from sqlmodel import SQLModel, Field
from zoneinfo import ZoneInfo

from src.security.security_handler import security_handler


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

# Faz o hash automaticamente antes de inserir
@event.listens_for(User, "before_insert")
def _hash_password_before_insert(mapper, connection, target: User) -> None:
    if target.password:
        target.password = security_handler.get_password_hash(target.password)

# Re-hash somente se a senha foi alterada durante update
@event.listens_for(User, "before_update")
def _hash_password_before_update(mapper, connection, target: User) -> None:
    state = inspect(target)
    if "password" in state.attrs:
        history = state.attrs.password.history
        if history.has_changes() and target.password:
            target.password = security_handler.get_password_hash(target.password)

