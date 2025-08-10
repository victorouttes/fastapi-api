from sqlmodel import SQLModel, Field

class Book(SQLModel, table=True):
    id: int = Field(primary_key=True)
    name: str
    price: int

class BookCreate(SQLModel):
    name: str
    price: int

class BookUpdate(SQLModel):
    name: str | None = None
    price: int | None = None

class BookPublic(SQLModel):
    name: str