from typing import Optional

from fastapi import Depends
from fastapi import status
from fastapi.exceptions import HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from jose import JWTError

from app.models.user import User
from app.services.hashing import Hasher
from app.services.user import get_user_by_username_for_auth
from config.config import setting

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login/token")


async def authenticate_user(username: str, password: str) -> Optional[User]:
    user = await get_user_by_username_for_auth(username=username)
    if user is None:
        return
    if not Hasher.verify_password(password, user.password):
        return
    return user


async def get_current_user_from_token(token: str = Depends(oauth2_scheme)):
    exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
    )
    try:
        payload = jwt.decode(token, setting.SECRET_KEY, algorithms=[setting.ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise exception
    except JWTError:
        raise exception
    user = await get_user_by_username_for_auth(username=username)
    if user is None:
        raise exception
    return user
