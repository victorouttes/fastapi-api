from http import HTTPStatus

from fastapi import APIRouter, Depends

from src.controllers.user_controller import UserController, user_controller
from src.models.entities.base import EntityList, DeletedMessage
from src.models.entities.user import UserPublic, UserCreate, UserUpdate

user_router = APIRouter(prefix="/users", tags=["users"])

@user_router.get("/", status_code=HTTPStatus.OK, response_model=EntityList[UserPublic])
async def list_users(page: int = 1, size: int = 10, controller: UserController = Depends(user_controller)):
    return await controller.get_paginated(page, size)

@user_router.post("/", status_code=HTTPStatus.CREATED, response_model=UserPublic)
async def create_user(user: UserCreate, controller: UserController = Depends(user_controller)):
    return await controller.create(data=user)

@user_router.get("/{id}", status_code=HTTPStatus.OK, response_model=UserPublic)
async def get_user(id: int, controller: UserController = Depends(user_controller)):
    return await controller.get_by_id(id)

@user_router.patch("/{id}", status_code=HTTPStatus.OK, response_model=UserPublic)
async def update_user(id: int, user: UserUpdate, controller: UserController = Depends(user_controller)):
    return await controller.update(id, data=user)

@user_router.delete("/{id}", status_code=HTTPStatus.OK, response_model=DeletedMessage)
async def delete_user(id: int, controller: UserController = Depends(user_controller)):
    await controller.delete(id)
    return {"message": "User deleted successfully"}
