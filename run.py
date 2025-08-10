from contextlib import asynccontextmanager

import fastapi
import uvicorn

from src.models.entities.book import Book
from src.models.repositories.book_repository import book_repository
from src.models.settings.db_init import init_db


@asynccontextmanager
async def lifespan(app: fastapi.FastAPI):
    await init_db()
    yield

app = fastapi.FastAPI(lifespan=lifespan)

@app.get('/books')
async def list_books():
    books: list[Book] = await book_repository.get_paginated()
    return books

@app.post('/books')
async def create_book(book: Book):
    book = await book_repository.create(name=book.name, price=book.price)
    return book

if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8000, workers=1)
