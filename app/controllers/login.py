from datetime import timedelta

from fastapi import APIRouter
from fastapi import Depends
from fastapi import status
from fastapi.exceptions import HTTPException
from fastapi.security import OAuth2PasswordRequestForm

from app.schemas.login import Token
from app.services.auth import authenticate_user
from app.services.security import create_access_token
from config.config import setting

login_router = APIRouter(prefix="/login", tags=["login"])


@login_router.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = await authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
        )
    access_token_expire = timedelta(minutes=setting.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username, "other_custom_data": [1, 2, 3, 4]},
        expires_delta=access_token_expire,
    )
    return {"access_token": access_token, "token_type": "bearer"}
