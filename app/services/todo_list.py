from typing import List
from typing import Optional
from uuid import UUID

from app.models.todo_list import ToDoList
from app.models.user import User
from app.repositories.todo_list import TodoListRepository
from app.schemas.todo_list import CreateTodoListSchema
from app.schemas.todo_list import ShowTodoListForCreateSchema
from app.schemas.todo_list import ShowTodoListSchema
from app.schemas.user import ShowUserSchema
from database.database import async_session


async def create_new_todo_list(
    body: CreateTodoListSchema, user: User
) -> ShowTodoListForCreateSchema:
    async with async_session() as session:
        async with session.begin():
            new_list = TodoListRepository(session)
            todo_list = await new_list.create_todo(
                name=body.name, description=body.description, user_id=user.id
            )
            return ShowTodoListForCreateSchema(
                id=todo_list.id,
                name=todo_list.name,
                description=todo_list.description,
                user=ShowUserSchema(
                    id=user.id,
                    username=user.username,
                    email=user.email,
                    is_active=user.is_active,
                ),
                created_at=todo_list.created_at,
                updated_at=todo_list.updated_at,
            )


async def get_all_todo_lists(user: User) -> List[ShowTodoListSchema]:
    async with async_session() as session:
        async with session.begin():
            lists_repo = TodoListRepository(session)
            user_lists = await lists_repo.get_all_user_lists(user.id)
            print(user_lists)
            return [
                ShowTodoListSchema(
                    id=user_list.id,
                    name=user_list.name,
                    description=user_list.description,
                    created_at=user_list.created_at,
                    updated_at=user_list.updated_at,
                )
                for user_list in user_lists
            ]


async def get_todo_list(list_id: UUID) -> Optional[ToDoList]:
    async with async_session() as session:
        list_repo = TodoListRepository(session)
        list = await list_repo.get_list_by_id(list_id)
        return list
