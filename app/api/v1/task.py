from logging import getLogger
from typing import List
from uuid import UUID

from fastapi import APIRouter
from fastapi import Depends
from fastapi.exceptions import RequestValidationError
from fastapi.responses import UJSONResponse
from sqlalchemy.exc import IntegrityError

from app.exceptions.exceptions import EmptyParametersException
from app.exceptions.exceptions import ObjectNotFoundException
from app.models.user import User
from app.schemas.task import CreateTaskSchema
from app.schemas.task import ShowTaskSchema
from app.schemas.task import UpdateTaskSchema
from app.services.auth import AuthService
from app.services.task import TaskService
from app.services.todo_list import TodoListService

logger = getLogger(__name__)

task_router = APIRouter()


@task_router.post("/", response_model=ShowTaskSchema)
async def create_tasks(
    body: CreateTaskSchema,
    current_user: User = Depends(AuthService.get_current_user_from_token),
):
    user_todo_lists = await TodoListService.get_all_todo_lists(current_user)
    if not any(user_list.id == body.todo_list_id for user_list in user_todo_lists):
        raise ObjectNotFoundException(
            detail=f"TodoList with id - {body.todo_list_id} is not found"
        )
    try:
        return await TaskService.create_new_task(body)
    except IntegrityError:
        raise
    except RequestValidationError:
        raise


@task_router.get("/", response_model=List[ShowTaskSchema])
async def get_all_user_tasks(
    current_user: User = Depends(AuthService.get_current_user_from_token),
):
    user_todo_lists = await TodoListService.get_all_todo_lists(current_user)
    try:
        return await TaskService.get_all_tasks(user_todo_lists)
    except IntegrityError:
        raise


@task_router.get("/{task_id}", response_model=ShowTaskSchema)
async def get_task_by_id(
    task_id: UUID,
    current_user: User = Depends(AuthService.get_current_user_from_token),
):
    user_todo_lists = await TodoListService.get_all_todo_lists(current_user)
    task = await TaskService.get_task(user_todo_lists, task_id)
    if task is None:
        raise ObjectNotFoundException(detail=f"Task with id - {task_id} is not found")
    return task


@task_router.patch("/{task_id}")
async def update_task(
    task_id: UUID,
    body: UpdateTaskSchema,
    current_user: User = Depends(AuthService.get_current_user_from_token),
):
    updated_params = body.model_dump(exclude_unset=True)
    if updated_params == {}:
        raise EmptyParametersException()
    user_todo_lists = await TodoListService.get_all_todo_lists(current_user)
    task = await TaskService.get_task(user_todo_lists, task_id)
    if task is None:
        raise ObjectNotFoundException(detail=f"Task with id - {task_id} is not found")
    try:
        await TaskService.update_user_task(task, updated_params)
    except IntegrityError:
        raise
    except RequestValidationError:
        raise
    else:
        return UJSONResponse(
            content={"detail": "Task successfully updated"}, status_code=201
        )


@task_router.delete("/{task_id}")
async def delete_task(
    task_id: UUID, current_user: User = Depends(AuthService.get_current_user_from_token)
):
    user_todo_lists = await TodoListService.get_all_todo_lists(current_user)
    task_for_deletion = await TaskService.get_task(user_todo_lists, task_id)
    if task_for_deletion is None:
        raise ObjectNotFoundException(detail=f"Task with id - {task_id} is not found")
    try:
        deleted_task = await TaskService.deleting_task(task_for_deletion)
        if deleted_task is None:
            return UJSONResponse(
                content={"detail": "Task was deleted successfully"}, status_code=200
            )
    except IntegrityError:
        raise
