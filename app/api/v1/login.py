from fastapi import APIRouter
from fastapi import Depends
from fastapi.security import OAuth2PasswordRequestForm

from app.schemas.login import Token
from app.services.auth import AuthService

login_router = APIRouter()


@login_router.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    access_token = await AuthService.authenticate_user(form_data)
    return {"access_token": access_token, "token_type": "bearer"}
