from fastapi import FastAPI

from app.controllers.login import login_router
from app.controllers.user import user_router

app = FastAPI()

app.include_router(user_router)
app.include_router(login_router)
