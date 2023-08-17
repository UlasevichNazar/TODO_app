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


class TodoListService:
    @staticmethod
    async def create_new_todo_list(
        body: CreateTodoListSchema, user_data: ShowUserSchema
    ) -> ShowTodoListForCreateSchema:
        async with async_session() as session:
            creation_todo = await TodoListService._create_todo_list(
                user_id=user_data.id, values=body
            )
            todo_list = await TodoListRepository(session).create_todo(creation_todo)
            session.commit()
            return ShowTodoListForCreateSchema(
                id=todo_list.id,
                name=todo_list.name,
                description=todo_list.description,
                user=user_data,
                created_at=todo_list.created_at,
                updated_at=todo_list.updated_at,
            )

    @staticmethod
    async def _create_todo_list(
        values: CreateTodoListSchema, user_id: UUID
    ) -> ToDoList:
        values_for_create = values.model_dump()
        values_for_create["user_id"] = user_id
        new_list = ToDoList(**values_for_create)
        return new_list

    @staticmethod
    async def get_all_todo_lists(user: User) -> List[ShowTodoListSchema]:
        async with async_session() as session:
            lists_repo = TodoListRepository(session)
            user_lists = await lists_repo.get_all_user_lists(user.id)
            return [user_list for user_list in user_lists]

    @staticmethod
    async def get_todo_list(list_id: UUID) -> Optional[ToDoList]:
        async with async_session() as session:
            list_repo = TodoListRepository(session)
            list = await list_repo.get_list_by_id(list_id)
            return list

    @staticmethod
    async def update_list(
        updated_params: dict, todo_list: ToDoList
    ) -> Result[ToDoList]:
        async with async_session() as session:
            updating_list = TodoListRepository(session)
            updated_todo_list = await updating_list.update_list_by_user(
                todo_list, **updated_params
            )
            session.commit()
            return updated_todo_list

    @staticmethod
    async def deleting_todo_list(list_id: UUID) -> Optional[UUID]:
        async with async_session() as session:
            deleting_list = TodoListRepository(session)
            deleting_list_id = await deleting_list.deleting_todo(list_id=list_id)
            session.commit()
            return deleting_list_id
