from logging import getLogger
from typing import List
from typing import Union
from uuid import UUID

from fastapi import APIRouter
from fastapi import Depends
from fastapi.exceptions import RequestValidationError
from fastapi.responses import UJSONResponse
from sqlalchemy.exc import IntegrityError

from app.exceptions.exceptions import EmptyParametersException
from app.exceptions.exceptions import ObjectNotFoundException
from app.exceptions.exceptions import PermissionDeniedException
from app.models.user import User
from app.permissions.user import UserPermissionsService
from app.schemas.user import CreateUserSchema
from app.schemas.user import ShowAdminSchema
from app.schemas.user import ShowUserSchema
from app.schemas.user import UpdateUserRequestSchema
from app.services.auth import AuthService
from app.services.user import UserService

logger = getLogger(__name__)

user_router = APIRouter()


@user_router.get("/", response_model=Union[List[ShowUserSchema], ShowUserSchema])
async def get_all_users_from_db(
    current_user: User = Depends(AuthService.get_current_user_from_token),
):
    try:
        return await UserService.get_all_users(current_user)
    except IntegrityError:
        raise


@user_router.get("/{user_id}", response_model=ShowUserSchema)
async def get_user_by_id(
    user_id: UUID, current_user: User = Depends(AuthService.get_current_user_from_token)
):
    user = await UserService.get_user(user_id)
    if user is None:
        raise ObjectNotFoundException(detail=f"User with id - {user_id} is not found.")
    if not await UserPermissionsService.check_user_permissions(
        target_user=user, current_user=current_user
    ):
        raise PermissionDeniedException()
    return user


@user_router.post("/", response_model=ShowUserSchema)
async def create_user(body: CreateUserSchema):
    try:
        return await UserService.create_new_user(body)
    except IntegrityError:
        raise
    except RequestValidationError:
        raise


@user_router.post("/admin", response_model=ShowAdminSchema)
async def create_admin_user(body: CreateUserSchema):
    try:
        return await UserService.create_admin(body)
    except IntegrityError:
        raise
    except RequestValidationError:
        raise


@user_router.patch("/{user_id}")
async def update_user_by_id(
    user_id: UUID,
    body: UpdateUserRequestSchema,
    current_user: User = Depends(AuthService.get_current_user_from_token),
):
    updated_params = body.model_dump(exclude_unset=True)
    if updated_params == {}:
        raise EmptyParametersException()
    user = await UserService.get_user(user_id)
    if not await UserPermissionsService.check_user_permissions(
        target_user=user, current_user=current_user
    ):
        raise PermissionDeniedException()
    try:
        await UserService.update_user(updated_params, user.id)
    except IntegrityError:
        raise
    except RequestValidationError:
        raise
    else:
        return UJSONResponse(
            content={"detail": "User successfully updated"}, status_code=201
        )


@user_router.delete("/{user_id}")
async def delete_user_by_id(
    user_id: UUID, current_user: User = Depends(AuthService.get_current_user_from_token)
):
    user_for_deletion = await UserService.get_user(user_id)
    if user_for_deletion is None:
        raise ObjectNotFoundException(detail=f"User with id - {user_id} is not found.")
    if not await UserPermissionsService.check_user_permissions(
        target_user=user_for_deletion, current_user=current_user
    ):
        raise PermissionDeniedException()
    deleted_user = await UserService.deleting_user(user_for_deletion)
    if deleted_user is None:
        return UJSONResponse(
            content={"detail": "User was deleted successfully."}, status_code=200
        )
