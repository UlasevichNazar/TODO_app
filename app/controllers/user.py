from logging import getLogger
from typing import List
from uuid import UUID

from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError

from app.models.user import User
from app.schemas.user import CreateUserSchema
from app.schemas.user import DeleteUserSchema
from app.schemas.user import ShowUserSchema
from app.schemas.user import UpdateUserRequestSchema
from app.schemas.user import UpdateUserResponseSchema
from app.services.auth import get_current_user_from_token
from app.services.user import check_user_permissions
from app.services.user import create_new_user
from app.services.user import deleting_user
from app.services.user import get_all_users
from app.services.user import get_user
from app.services.user import get_user_by_id_for_del
from app.services.user import update_user

logger = getLogger(__name__)

user_router = APIRouter(prefix="/user", tags=["user"])


@user_router.get("/", response_model=List[ShowUserSchema])
async def get_all_users_from_db(
    current_user: User = Depends(get_current_user_from_token),
):
    return await get_all_users()


@user_router.get("/{user_id}", response_model=ShowUserSchema)
async def get_user_by_id(
    user_id: UUID, current_user: User = Depends(get_current_user_from_token)
) -> ShowUserSchema:
    user = await get_user(user_id)
    if user is None:
        raise HTTPException(
            status_code=404, detail=f"User with {user_id} is not found."
        )
    return user


@user_router.post("/", response_model=ShowUserSchema)
async def create_user(body: CreateUserSchema):
    return await create_new_user(body)


@user_router.patch("/{user_id}", response_model=UpdateUserResponseSchema)
async def update_user_by_id(
    user_id: UUID,
    body: UpdateUserRequestSchema,
    current_user: User = Depends(get_current_user_from_token),
) -> UpdateUserResponseSchema:
    updated_user_params = body.model_dump(exclude_none=True)
    if updated_user_params == {}:
        raise HTTPException(
            status_code=422,
            detail="At least one parameter for user update info should be provided",
        )
    user_for_update = await get_user_by_id(user_id)
    if user_for_update is None:
        raise HTTPException(
            status_code=404, detail=f"User with id {user_id} not found."
        )
    try:
        updated_user_id = await update_user(
            updated_user_params=updated_user_params, user_id=user_id
        )
    except IntegrityError as err:
        logger.error(err)
        raise HTTPException(status_code=503, detail=f"Database error: {err}")
    return UpdateUserResponseSchema(user_id=updated_user_id)


@user_router.delete("/{user_id}", response_model=DeleteUserSchema)
async def delete_user_by_id(
    user_id: UUID, current_user: User = Depends(get_current_user_from_token)
) -> DeleteUserSchema:
    user_for_deletion = await get_user_by_id_for_del(user_id)
    if user_for_deletion is None:
        raise HTTPException(
            status_code=404, detail=f"User with {user_id} is not found."
        )
    if not await check_user_permissions(
        target_user=user_for_deletion, current_user=current_user
    ):
        print(1)
        raise HTTPException(status_code=403, detail="Forbidden.")

    deleted_user_id = await deleting_user(user_id)
    print(deleted_user_id)
    if deleted_user_id is None:
        raise HTTPException(
            status_code=404, detail=f"User with {user_id} is not found."
        )

    return DeleteUserSchema(delete_user_id=deleted_user_id)
