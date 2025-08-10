from src.controllers.base_controller import BaseController
from src.models.entities.book import Book, BookCreate, BookUpdate
from src.models.repositories.book_repository import BookRepository


class BookController(BaseController[Book, BookCreate, BookUpdate, BookRepository]):
    pass

book_controller = BookController
