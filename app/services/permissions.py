from fastapi import HTTPException

from app.models.user import Roles
from app.models.user import User


class PermissionsService:
    @staticmethod
    async def check_user_permissions(target_user: User, current_user: User) -> bool:
        if target_user.id == current_user.id:
            return True

        if Roles.ROLE_ADMIN in current_user.roles:
            return True

        if Roles.ROLE_ADMIN in target_user.roles:
            raise HTTPException(
                status_code=406,
                detail="You dont have any permissions to perform this action",
            )

        return False
