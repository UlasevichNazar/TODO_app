from logging import getLogger
from typing import List
from typing import Union
from uuid import UUID

from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from fastapi import Request
from fastapi import Response
from fastapi.exceptions import RequestValidationError
from sqlalchemy.exc import IntegrityError

from app.exceptions import validation_exception_handler
from app.models.user import User
from app.permissions.user import UserPermissionsService
from app.schemas.user import CreateUserSchema
from app.schemas.user import DeleteUserSchema
from app.schemas.user import ShowAdminSchema
from app.schemas.user import ShowUserSchema
from app.schemas.user import UpdateUserRequestSchema
from app.services.auth import get_current_user_from_token
from app.services.user import create_admin
from app.services.user import create_new_user
from app.services.user import deleting_user
from app.services.user import get_all_users
from app.services.user import get_user
from app.services.user import update_user

logger = getLogger(__name__)

user_router = APIRouter(prefix="/user", tags=["user"])


@user_router.get("/", response_model=Union[List[ShowUserSchema], ShowUserSchema])
async def get_all_users_from_db(
    current_user: User = Depends(get_current_user_from_token),
):
    try:
        return await get_all_users(current_user)

    except IntegrityError as err:
        raise HTTPException(status_code=503, detail=f"Database error: {err}")


@user_router.get("/{user_id}", response_model=ShowUserSchema)
async def get_user_by_id(
    user_id: UUID, current_user: User = Depends(get_current_user_from_token)
) -> ShowUserSchema:
    user = await get_user(user_id)
    if user is None:
        raise HTTPException(
            status_code=404, detail=f"User with {user_id} is not found."
        )
    if not await UserPermissionsService.check_user_permissions(
        target_user=user, current_user=current_user
    ):
        raise HTTPException(status_code=403, detail="Forbidden.")
    return user


@user_router.post("/", response_model=ShowUserSchema)
async def create_user(body: CreateUserSchema):
    try:
        return await create_new_user(body)
    except IntegrityError as err:
        raise HTTPException(status_code=503, detail=f"Database error: {err}")
    except RequestValidationError as exc:
        return await validation_exception_handler(Request, exc)


@user_router.post("/admin", response_model=ShowAdminSchema)
async def create_admin_user(body: CreateUserSchema):
    try:
        return await create_admin(body)
    except IntegrityError as err:
        raise HTTPException(status_code=503, detail=f"Database error: {err}")
    except RequestValidationError as exc:
        return await validation_exception_handler(Request, exc)


@user_router.patch("/{user_id}")
async def update_user_by_id(
    user_id: UUID,
    body: UpdateUserRequestSchema,
    current_user: User = Depends(get_current_user_from_token),
):
    updated_params = body.model_dump(exclude_unset=True)
    if updated_params == {}:
        raise HTTPException(
            status_code=422,
            detail="At least one parameter for task update info should be provided",
        )
    user = await get_user(user_id)
    if not await UserPermissionsService.check_user_permissions(
        target_user=user, current_user=current_user
    ):
        raise HTTPException(status_code=403, detail="Forbidden.")
    try:
        await update_user(updated_params, user.id)
    except IntegrityError as err:
        raise HTTPException(status_code=503, detail=f"Database error: {err}")
    except RequestValidationError as exc:
        return await validation_exception_handler(Request, exc)
    else:
        return Response("User successfully updated", status_code=201)


@user_router.delete("/{user_id}", response_model=DeleteUserSchema)
async def delete_user_by_id(
    user_id: UUID, current_user: User = Depends(get_current_user_from_token)
) -> DeleteUserSchema:
    user_for_deletion = await get_user(user_id)
    if user_for_deletion is None:
        raise HTTPException(
            status_code=404, detail=f"User with {user_id} is not found."
        )
    if not await UserPermissionsService.check_user_permissions(
        target_user=user_for_deletion, current_user=current_user
    ):
        raise HTTPException(status_code=403, detail="Forbidden.")

    deleted_user_id = await deleting_user(user_id)

    return DeleteUserSchema(delete_user_id=deleted_user_id)
