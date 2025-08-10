from sqlmodel import SQLModel, Field

class Book(SQLModel, table=True):
    id: int = Field(primary_key=True)
    name: str
    price: int
