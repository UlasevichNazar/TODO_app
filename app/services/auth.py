from datetime import datetime
from datetime import timedelta
from typing import Optional
from typing import Union

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from fastapi.security import OAuth2PasswordRequestForm
from jose import jwt
from jose import JWTError

from app.exceptions.exceptions import AutorizingException
from app.models.user import User
from app.services.user import UserService
from app.utils.password_hasher import PasswordService
from config.config import setting

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/v1/login/token")


class AuthService:
    @staticmethod
    async def _authenticate_user(username: str, password: str) -> Union[User, None]:
        user = await UserService.get_user_by_username_for_auth(username=username)
        if user is None:
            return None
        if not PasswordService.verify_password(password, user.password):
            return None
        return user

    @staticmethod
    async def authenticate_user(form_data: OAuth2PasswordRequestForm):
        user = await AuthService._authenticate_user(
            username=form_data.username,
            password=form_data.password,
        )
        if not user:
            raise AutorizingException(detail="Incorrect username or password")
        return await AuthService.generate_token(user)

    @staticmethod
    async def generate_token(user: User):
        access_token_expire = timedelta(minutes=setting.ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = await AuthService.create_access_token(
            data={"sub": user.username}, expires_delta=access_token_expire
        )
        return access_token

    @staticmethod
    async def get_current_user_from_token(token: str = Depends(oauth2_scheme)):
        try:
            payload = jwt.decode(
                token, setting.SECRET_KEY, algorithms=[setting.ALGORITHM]
            )
            username: str = payload.get("sub")
            if username is None:
                raise AutorizingException()
        except JWTError:
            raise AutorizingException()
        user = await UserService.get_user_by_username_for_auth(username=username)
        if user is None:
            raise AutorizingException()
        return user

    @staticmethod
    async def create_access_token(
        data: dict, expires_delta: Optional[timedelta] = None
    ):
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(
                minutes=setting.ACCESS_TOKEN_EXPIRE_MINUTES
            )

        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, setting.SECRET_KEY, setting.ALGORITHM)
        return encoded_jwt
