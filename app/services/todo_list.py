from typing import List
from typing import Optional
from uuid import UUID

from sqlalchemy import Result

from app.models.todo_list import ToDoList
from app.models.user import User
from app.repositories.todo_list import TodoListRepository
from app.schemas.todo_list import CreateTodoListSchema
from app.schemas.todo_list import ShowTodoListForCreateSchema
from app.schemas.todo_list import ShowTodoListSchema
from app.schemas.user import ShowUserSchema
from database.database import async_session


async def create_new_todo_list(
    body: CreateTodoListSchema, user_data: ShowUserSchema
) -> ShowTodoListForCreateSchema:
    async with async_session() as session:
        async with session.begin():
            new_list = TodoListRepository(session)
            todo_list = await new_list.create_todo(user_id=user_data.id, values=body)
            session.commit()
            return ShowTodoListForCreateSchema(
                id=todo_list.id,
                name=todo_list.name,
                description=todo_list.description,
                user=user_data,
                created_at=todo_list.created_at,
                updated_at=todo_list.updated_at,
            )


async def get_all_todo_lists(user: User) -> List[ShowTodoListSchema]:
    async with async_session() as session:
        async with session.begin():
            lists_repo = TodoListRepository(session)
            user_lists = await lists_repo.get_all_user_lists(user.id)
            return [user_list for user_list in user_lists]


async def get_todo_list(list_id: UUID) -> Optional[ToDoList]:
    async with async_session() as session:
        async with session.begin():
            list_repo = TodoListRepository(session)
            list = await list_repo.get_list_by_id(list_id)
            return list


async def update_list(updated_params: dict, todo_list: ToDoList) -> Result[ToDoList]:
    async with async_session() as session:
        async with session.begin():
            updating_list = TodoListRepository(session)
            updated_todo_list = await updating_list.update_list_by_user(
                todo_list, **updated_params
            )
            session.commit()
            return updated_todo_list


async def deleting_todo_list(list_id: UUID) -> Optional[UUID]:
    async with async_session() as session:
        async with session.begin():
            deleting_list = TodoListRepository(session)
            deleting_list_id = await deleting_list.deleting_todo(list_id=list_id)
            session.commit()
            return deleting_list_id
