from fastapi import FastAPI

from app.user.controllers import user_router

app = FastAPI()

app.include_router(user_router)
