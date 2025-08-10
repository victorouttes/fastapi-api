from src.models.entities.book import Book
from src.models.repositories.base_repository import BaseRepository


class BookRepository(BaseRepository[Book]):
    pass

book_repository = BookRepository()
