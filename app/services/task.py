from typing import List
from typing import Optional
from uuid import UUID

from app.models.task import Task
from app.repositories.task import TaskRepository
from app.schemas.task import CreateTaskSchema
from app.schemas.task import ShowTaskSchema
from app.schemas.todo_list import ShowTodoListSchema
from database.database import async_session


async def create_new_task(body: CreateTaskSchema) -> ShowTaskSchema:
    async with async_session() as session:
        async with session.begin():
            new_task = TaskRepository(session)
            task = await new_task.create_new_task(
                name=body.name,
                description=body.description,
                todo_list_id=body.todo_list_id,
            )
            session.commit()
            return ShowTaskSchema(
                id=task.id,
                name=task.name,
                description=task.description,
                status=task.status,
                todo_list_id=task.todo_list_id,
            )


async def get_all_tasks(todo_lists: List[ShowTodoListSchema]) -> List[ShowTaskSchema]:
    async with async_session() as session:
        async with session.begin():
            tasks_repo = TaskRepository(session)
            todo_list_ids = tuple(user_list.id for user_list in todo_lists)
            list_of_tasks = await tasks_repo.get_tasks(todo_list_ids)
            return [
                ShowTaskSchema(
                    id=list_of_task.id,
                    name=list_of_task.name,
                    description=list_of_task.description,
                    status=list_of_task.status,
                    todo_list_id=list_of_task.todo_list_id,
                )
                for list_of_task in list_of_tasks
            ]


async def get_task(
    todo_lists: List[ShowTodoListSchema], task_id: UUID
) -> Optional[Task]:
    async with async_session() as session:
        async with session.begin():
            tasks_repo = TaskRepository(session)
            todo_list_ids = tuple(user_list.id for user_list in todo_lists)
            task = await tasks_repo.get_user_task(task_id, todo_list_ids)
            return task
