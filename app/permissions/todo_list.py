from app.models.todo_list import ToDoList
from app.models.user import User


class TodoListPermissionsService:
    @staticmethod
    async def check_user_permissions(todo_list: ToDoList, current_user: User) -> bool:
        if todo_list.user_id == current_user.id:
            return True
        return False
