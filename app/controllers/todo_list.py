from logging import getLogger
from typing import List
from uuid import UUID

from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError

from app.models.user import User
from app.permissions.todo_list import TodoListPermissionsService
from app.schemas.todo_list import CreateTodoListSchema
from app.schemas.todo_list import ShowTodoListForCreateSchema
from app.schemas.todo_list import ShowTodoListSchema
from app.services.auth import get_current_user_from_token
from app.services.todo_list import create_new_todo_list
from app.services.todo_list import get_all_todo_lists
from app.services.todo_list import get_todo_list

logger = getLogger(__name__)

todo_list_router = APIRouter(prefix="/todo_list", tags=["todo_list "])


@todo_list_router.post("/", response_model=ShowTodoListForCreateSchema)
async def create_todo_list(
    body: CreateTodoListSchema,
    current_user: User = Depends(get_current_user_from_token),
):
    try:
        return await create_new_todo_list(body, current_user)

    except IntegrityError as err:
        logger.info(err)
        raise HTTPException(status_code=503, detail=f"Database error: {err}")


@todo_list_router.get("/", response_model=List[ShowTodoListSchema])
async def get_all_lists(current_user: User = Depends(get_current_user_from_token)):
    try:
        return await get_all_todo_lists(current_user)
    except IntegrityError as err:
        raise HTTPException(status_code=503, detail=f"Database error: {err}")


@todo_list_router.get("/{list_id}", response_model=ShowTodoListSchema)
async def get_todo_list_by_id(
    list_id: UUID, current_user: User = Depends(get_current_user_from_token)
):
    todo_list = await get_todo_list(list_id)

    if todo_list is None:
        raise HTTPException(status_code=404, detail="Todo List is not found")
    if not await TodoListPermissionsService.check_user_permissions(
        todo_list=todo_list, current_user=current_user
    ):
        raise HTTPException(status_code=403, detail="Forbidden")
    return todo_list
