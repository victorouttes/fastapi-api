from fastapi import APIRouter, Depends

from src.controllers.book_controller import BookController, book_controller
from src.models.entities.book import Book

book_router = APIRouter(prefix="/books", tags=["books"])

@book_router.get("/")
async def list_books(page: int = 1, size: int = 10, controller: BookController = Depends(book_controller)):
    return await controller.get_paginated(page, size)

@book_router.post("/", status_code=201, response_model=Book)
async def create_book(book: Book, controller: BookController = Depends(book_controller)):
    return await controller.create(name=book.name, price=book.price)

@book_router.get("/{id}", response_model=Book)
async def get_book(id: int, controller: BookController = Depends(book_controller)):
    return await controller.get_by_id(id)

@book_router.put("/{id}", status_code=204)
async def update_book(id: int, book: Book, controller: BookController = Depends(book_controller)):
    return await controller.update(id, name=book.name, price=book.price)

@book_router.delete("/{id}", status_code=204)
async def delete_book(id: int, controller: BookController = Depends(book_controller)):
    if await controller.delete(id):
        return {"message": "Book deleted successfully"}
    else:
        return {"message": "Book not found"}
