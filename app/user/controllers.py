from fastapi import APIRouter

user_router = APIRouter(prefix="/user")


@user_router.post("/create")
async def create_user():
    pass
