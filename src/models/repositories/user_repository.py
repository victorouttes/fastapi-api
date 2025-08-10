from src.models.entities.user import User, UserCreate, UserUpdate
from src.models.repositories.base_repository import BaseRepository


class UserRepository(BaseRepository[User, UserCreate, UserUpdate]):
    pass

book_repository = UserRepository()
