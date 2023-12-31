from typing import List
from typing import Optional
from uuid import UUID

from sqlalchemy import Result

from app.models.task import Task
from app.repositories.task import TaskRepository
from app.schemas.task import CreateTaskSchema
from app.schemas.task import ShowTaskSchema
from app.schemas.todo_list import ShowTodoListSchema
from database.database import async_session


class TaskService:
    @staticmethod
    async def create_new_task(body: CreateTaskSchema) -> Task:
        async with async_session() as session:
            new_task = TaskRepository(session)
            task = await new_task.create_new_task(body)
            await session.commit()
            return task

    @staticmethod
    async def get_all_tasks(
        todo_lists: List[ShowTodoListSchema],
    ) -> List[ShowTaskSchema]:
        async with async_session() as session:
            tasks_repo = TaskRepository(session)
            todo_list_ids = tuple(user_list.id for user_list in todo_lists)
            list_of_tasks = await tasks_repo.get_tasks(todo_list_ids)
            return [list_of_task for list_of_task in list_of_tasks]

    @staticmethod
    async def get_task(
        todo_lists: List[ShowTodoListSchema], task_id: UUID
    ) -> Optional[Task]:
        async with async_session() as session:
            tasks_repo = TaskRepository(session)
            todo_list_ids = tuple(user_list.id for user_list in todo_lists)
            task = await tasks_repo.get_user_task(task_id, todo_list_ids)
            return task

    @staticmethod
    async def update_user_task(task: Task, updated_params: dict) -> Result[Task]:
        async with async_session() as session:
            updating_task = TaskRepository(session)
            updated_task = await updating_task.updating_task_by_user(
                task, **updated_params
            )
            await session.commit()
            return updated_task

    @staticmethod
    async def deleting_task(task: Task) -> None:
        async with async_session() as session:
            task_repo = TaskRepository(session)
            deleting_task_id = await task_repo.deleting_task_by_user(task)
            await session.commit()
            return deleting_task_id
