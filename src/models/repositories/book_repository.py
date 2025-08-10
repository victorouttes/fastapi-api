from src.models.entities.book import Book, BookCreate, BookUpdate
from src.models.repositories.base_repository import BaseRepository


class BookRepository(BaseRepository[Book, BookCreate, BookUpdate]):
    pass

book_repository = BookRepository()
