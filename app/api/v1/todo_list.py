from logging import getLogger
from typing import List
from uuid import UUID

from fastapi import APIRouter
from fastapi import Depends
from fastapi.exceptions import RequestValidationError
from fastapi.responses import UJSONResponse
from sqlalchemy.exc import IntegrityError

from app.api.v1.user import get_user_by_id
from app.exceptions.exceptions import EmptyParametersException
from app.exceptions.exceptions import ObjectNotFoundException
from app.exceptions.exceptions import PermissionDeniedException
from app.models.user import User
from app.permissions.todo_list import TodoListPermissionsService
from app.schemas.todo_list import CreateTodoListSchema
from app.schemas.todo_list import ShowTodoListForCreateSchema
from app.schemas.todo_list import ShowTodoListSchema
from app.schemas.todo_list import UpdateTodoListSchema
from app.services.auth import AuthService
from app.services.todo_list import TodoListService

logger = getLogger(__name__)

todo_list_router = APIRouter()


@todo_list_router.post("/", response_model=ShowTodoListForCreateSchema)
async def create_todo_list(
    body: CreateTodoListSchema,
    current_user: User = Depends(AuthService.get_current_user_from_token),
):
    try:
        user_data = await get_user_by_id(current_user.id, current_user)
        return await TodoListService.create_new_todo_list(body, user_data)
    except IntegrityError:
        raise
    except RequestValidationError:
        raise


@todo_list_router.get("/", response_model=List[ShowTodoListSchema])
async def get_all_lists(
    current_user: User = Depends(AuthService.get_current_user_from_token),
):
    try:
        return await TodoListService.get_all_todo_lists(current_user)
    except IntegrityError:
        raise


@todo_list_router.get("/{list_id}", response_model=ShowTodoListSchema)
async def get_todo_list_by_id(
    list_id: UUID, current_user: User = Depends(AuthService.get_current_user_from_token)
):
    todo_list = await TodoListService.get_todo_list(list_id)

    if todo_list is None:
        raise ObjectNotFoundException(
            detail=f"Todo List with id - {list_id} is not found."
        )
    if not await TodoListPermissionsService.check_user_permissions(
        todo_list=todo_list, current_user=current_user
    ):
        raise PermissionDeniedException()
    return todo_list


@todo_list_router.patch("/{list_id}")
async def update_todo_list(
    list_id: UUID,
    body: UpdateTodoListSchema,
    current_user: User = Depends(AuthService.get_current_user_from_token),
):
    updated_params = body.model_dump(exclude_unset=True)
    if updated_params == {}:
        raise EmptyParametersException()
    todo_list = await TodoListService.get_todo_list(list_id)
    if todo_list is None:
        raise ObjectNotFoundException(
            detail=f"Todo List with id - {list_id} is not found."
        )
    if not await TodoListPermissionsService.check_user_permissions(
        todo_list=todo_list, current_user=current_user
    ):
        raise PermissionDeniedException()
    try:
        await TodoListService.update_list(updated_params, todo_list)
    except IntegrityError:
        raise
    except RequestValidationError:
        raise
    else:
        return UJSONResponse(
            content={"detail": "Todo List successfully updated"}, status_code=201
        )


@todo_list_router.delete("/{list_id}")
async def delete_todo_list(
    list_id: UUID, current_user: User = Depends(AuthService.get_current_user_from_token)
):
    list_for_deletion = await TodoListService.get_todo_list(list_id)
    if list_for_deletion is None:
        raise ObjectNotFoundException(
            detail=f"Todo List with id - {list_id} is not found."
        )
    if not await TodoListPermissionsService.check_user_permissions(
        todo_list=list_for_deletion, current_user=current_user
    ):
        raise PermissionDeniedException()
    deleted_todo_list = await TodoListService.deleting_todo_list(list_for_deletion)
    if deleted_todo_list is None:
        return UJSONResponse(
            content={"detail": "Todo List was deleted successfully."}, status_code=200
        )
