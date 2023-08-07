from fastapi import FastAPI

from app.controllers.user import user_router

app = FastAPI()

app.include_router(user_router)
