from fastapi import APIRouter

user_router = APIRouter(prefix="/users")


@user_router.get("/create")
async def create_user():
    pass
