from logging import getLogger
from typing import List
from uuid import UUID

from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError

from app.models.user import User
from app.schemas.task import CreateTaskSchema
from app.schemas.task import ShowTaskSchema
from app.services.auth import get_current_user_from_token
from app.services.task import create_new_task
from app.services.task import get_all_tasks
from app.services.task import get_task
from app.services.todo_list import get_all_todo_lists

logger = getLogger(__name__)

task_router = APIRouter(prefix="/task", tags=["task"])


@task_router.post("/", response_model=ShowTaskSchema)
async def create_tasks(
    body: CreateTaskSchema,
    current_user: User = Depends(get_current_user_from_token),
):
    user_todo_lists = await get_all_todo_lists(current_user)
    if not any(user_list.id == body.todo_list_id for user_list in user_todo_lists):
        raise HTTPException(
            status_code=404,
            detail=f"TodoList with id - {body.todo_list_id} is not found",
        )
    try:
        return await create_new_task(body)
    except IntegrityError as err:
        logger.info(err)
        raise HTTPException(status_code=503, detail=f"Database error: {err}")


@task_router.get("/", response_model=List[ShowTaskSchema])
async def get_all_user_tasks(
    current_user: User = Depends(get_current_user_from_token),
):
    user_todo_lists = await get_all_todo_lists(current_user)

    try:
        return await get_all_tasks(user_todo_lists)
    except IntegrityError as err:
        logger.info(err)
        raise HTTPException(status_code=503, detail=f"Database error: {err}")


@task_router.get("/{task_id}", response_model=ShowTaskSchema)
async def get_task_by_id(
    task_id: UUID,
    current_user: User = Depends(get_current_user_from_token),
):
    user_todo_lists = await get_all_todo_lists(current_user)
    task = await get_task(user_todo_lists, task_id)
    if task is None:
        raise HTTPException(
            status_code=404, detail=f"Task with id - {task_id} is not found"
        )
    return task
