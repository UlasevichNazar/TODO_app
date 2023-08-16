from logging import getLogger
from typing import List
from uuid import UUID

from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from fastapi import Request
from fastapi import Response
from fastapi.exceptions import RequestValidationError
from sqlalchemy.exc import IntegrityError

from app.controllers.user import get_user_by_id
from app.exceptions import validation_exception_handler
from app.models.user import User
from app.permissions.todo_list import TodoListPermissionsService
from app.schemas.todo_list import CreateTodoListSchema
from app.schemas.todo_list import DeleteTodoListSchema
from app.schemas.todo_list import ShowTodoListForCreateSchema
from app.schemas.todo_list import ShowTodoListSchema
from app.schemas.todo_list import UpdateTodoListSchema
from app.services.auth import get_current_user_from_token
from app.services.todo_list import create_new_todo_list
from app.services.todo_list import deleting_todo_list
from app.services.todo_list import get_all_todo_lists
from app.services.todo_list import get_todo_list
from app.services.todo_list import update_list

logger = getLogger(__name__)

todo_list_router = APIRouter(prefix="/todo_list", tags=["todo_list "])


@todo_list_router.post("/", response_model=ShowTodoListForCreateSchema)
async def create_todo_list(
    body: CreateTodoListSchema,
    current_user: User = Depends(get_current_user_from_token),
):
    try:
        user_data = await get_user_by_id(current_user.id, current_user)
        return await create_new_todo_list(body, user_data)

    except IntegrityError as err:
        raise HTTPException(status_code=503, detail=f"Database error: {err}")
    except RequestValidationError as exc:
        return await validation_exception_handler(Request, exc)


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


@todo_list_router.patch("/{list_id}")
async def update_todo_list(
    list_id: UUID,
    body: UpdateTodoListSchema,
    current_user: User = Depends(get_current_user_from_token),
):
    updated_params = body.model_dump(exclude_unset=True)
    if updated_params == {}:
        raise HTTPException(
            status_code=422,
            detail="At least one parameter for task update info should be provided",
        )
    todo_list = await get_todo_list(list_id)
    if todo_list is None:
        raise HTTPException(
            status_code=404, detail=f"Todo List with id - {list_id} is not found."
        )
    if not await TodoListPermissionsService.check_user_permissions(
        todo_list=todo_list, current_user=current_user
    ):
        raise HTTPException(status_code=403, detail="Forbidden.")
    try:
        await update_list(updated_params, todo_list)
    except IntegrityError as err:
        raise HTTPException(status_code=503, detail=f"Database error: {err}")
    except RequestValidationError as exc:
        return await validation_exception_handler(Request, exc)
    else:
        return Response("Todo List successfully updated", status_code=201)


@todo_list_router.delete("/{list_id}", response_model=DeleteTodoListSchema)
async def delete_todo_list(
    list_id: UUID, current_user: User = Depends(get_current_user_from_token)
) -> DeleteTodoListSchema:
    list_for_deletion = await get_todo_list(list_id)
    if list_for_deletion is None:
        raise HTTPException(
            status_code=404, detail=f"TodoList with {list_id} is not found."
        )
    if not await TodoListPermissionsService.check_user_permissions(
        todo_list=list_for_deletion, current_user=current_user
    ):
        raise HTTPException(status_code=403, detail="Forbidden.")
    deleted_todo_list = await deleting_todo_list(list_id)
    return DeleteTodoListSchema(deleted_todo_list_id=deleted_todo_list)
