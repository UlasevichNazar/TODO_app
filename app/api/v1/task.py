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

from app.exceptions.exceptions import ExceptionService
from app.models.user import User
from app.schemas.task import CreateTaskSchema
from app.schemas.task import DeleteTaskSchema
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
        raise HTTPException(
            status_code=404,
            detail=f"TodoList with id - {body.todo_list_id} is not found",
        )
    try:
        return await TaskService.create_new_task(body)
    except IntegrityError as err:
        error_message = await ExceptionService.get_error_message("".join(err.args))
        raise HTTPException(status_code=503, detail=f"{error_message}")
    except RequestValidationError as exc:
        return await ExceptionService.validation_exception_handler(Request, exc)


@task_router.get("/", response_model=List[ShowTaskSchema])
async def get_all_user_tasks(
    current_user: User = Depends(AuthService.get_current_user_from_token),
):
    user_todo_lists = await TodoListService.get_all_todo_lists(current_user)

    try:
        return await TaskService.get_all_tasks(user_todo_lists)
    except IntegrityError as err:
        error_message = await ExceptionService.get_error_message("".join(err.args))
        raise HTTPException(status_code=503, detail=f"{error_message}")


@task_router.get("/{task_id}", response_model=ShowTaskSchema)
async def get_task_by_id(
    task_id: UUID,
    current_user: User = Depends(AuthService.get_current_user_from_token),
):
    user_todo_lists = await TodoListService.get_all_todo_lists(current_user)
    task = await TaskService.get_task(user_todo_lists, task_id)
    if task is None:
        raise HTTPException(
            status_code=404, detail=f"Task with id - {task_id} is not found"
        )
    return task


@task_router.patch("/{task_id}")
async def update_task(
    task_id: UUID,
    body: UpdateTaskSchema,
    current_user: User = Depends(AuthService.get_current_user_from_token),
):
    updated_params = body.model_dump(exclude_unset=True)
    if updated_params == {}:
        raise HTTPException(
            status_code=422,
            detail="At least one parameter for task update info should be provided",
        )
    user_todo_lists = await TodoListService.get_all_todo_lists(current_user)
    task = await TaskService.get_task(user_todo_lists, task_id)
    if task is None:
        raise HTTPException(
            status_code=404, detail=f"Task with id - {task_id} is not found"
        )
    try:
        await TaskService.update_user_task(task, updated_params)
    except IntegrityError as err:
        error_message = await ExceptionService.get_error_message("".join(err.args))
        raise HTTPException(status_code=503, detail=f"{error_message}")
    except RequestValidationError as exc:
        return await ExceptionService.validation_exception_handler(Request, exc)
    else:
        return Response("Task successfully updated", status_code=201)


@task_router.delete("/{task_id}", response_model=DeleteTaskSchema)
async def delete_task(
    task_id: UUID, current_user: User = Depends(AuthService.get_current_user_from_token)
):
    user_todo_lists = await TodoListService.get_all_todo_lists(current_user)
    task_for_deletion = await TaskService.get_task(user_todo_lists, task_id)
    if task_for_deletion is None:
        raise HTTPException(
            status_code=404, detail=f"Task with id - {task_id} is not found"
        )
    try:
        deleted_task = await TaskService.deleting_task(task_id)
    except IntegrityError as err:
        error_message = await ExceptionService.get_error_message("".join(err.args))
        raise HTTPException(status_code=503, detail=f"{error_message}")
    else:
        return DeleteTaskSchema(deleted_task_id=deleted_task)
