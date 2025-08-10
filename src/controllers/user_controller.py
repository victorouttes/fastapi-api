from src.controllers.base_controller import BaseController
from src.models.entities.user import User, UserCreate, UserUpdate
from src.models.repositories.user_repository import UserRepository


class UserController(BaseController[User, UserCreate, UserUpdate, UserRepository]):
    pass

user_controller = UserController
