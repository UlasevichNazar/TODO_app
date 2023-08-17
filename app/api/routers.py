from fastapi import APIRouter

from app.api.v1.login import login_router
from app.api.v1.task import task_router
from app.api.v1.todo_list import todo_list_router
from app.api.v1.user import user_router

v1_router = APIRouter(prefix="/v1")

v1_router.include_router(user_router, prefix="/user", tags=["user"])
v1_router.include_router(task_router, prefix="/task", tags=["task"])
v1_router.include_router(login_router, prefix="/login", tags=["login"])
v1_router.include_router(todo_list_router, prefix="/todo_list", tags=["todo_list "])
