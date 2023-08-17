from app import app
from app.api.routers import v1_router

app.include_router(v1_router, prefix="/api")
