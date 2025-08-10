from http import HTTPStatus

from fastapi import APIRouter, Depends

from src.controllers.book_controller import BookController, book_controller
from src.models.entities.base import EntityList, DeletedMessage
from src.models.entities.book import BookPublic, BookCreate, BookUpdate

book_router = APIRouter(prefix="/books", tags=["books"])

@book_router.get("/", status_code=HTTPStatus.OK, response_model=EntityList[BookPublic])
async def list_books(page: int = 1, size: int = 10, controller: BookController = Depends(book_controller)):
    return await controller.get_paginated(page, size)

@book_router.post("/", status_code=HTTPStatus.CREATED, response_model=BookPublic)
async def create_book(book: BookCreate, controller: BookController = Depends(book_controller)):
    return await controller.create(data=book)

@book_router.get("/{id}", status_code=HTTPStatus.OK, response_model=BookPublic)
async def get_book(id: int, controller: BookController = Depends(book_controller)):
    return await controller.get_by_id(id)

@book_router.put("/{id}", status_code=HTTPStatus.OK, response_model=BookPublic)
async def update_book(id: int, book: BookUpdate, controller: BookController = Depends(book_controller)):
    return await controller.update(id, data=book)

@book_router.delete("/{id}", status_code=HTTPStatus.OK, response_model=DeletedMessage)
async def delete_book(id: int, controller: BookController = Depends(book_controller)):
    await controller.delete(id)
    return {"message": "Book deleted successfully"}
