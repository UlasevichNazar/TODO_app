from fastapi import FastAPI

from app.api.routers import v1_router
from app.handlers import add_exception_handlers


def init_app() -> FastAPI:
    app = FastAPI()
    add_exception_handlers(app=app)
    app.include_router(v1_router, prefix="/api")
    return app
