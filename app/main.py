from app.controllers import app
from app.controllers.login import login_router
from app.controllers.task import task_router
from app.controllers.todo_list import todo_list_router
from app.controllers.user import user_router

app.include_router(user_router)
app.include_router(login_router)
app.include_router(task_router)
app.include_router(todo_list_router)
