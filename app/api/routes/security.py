from typing import Annotated

from app.api.dependencies import create_token, get_current_active_user
from app.config import ALLOW_REGISTER
from app.models import RegisterUserRequest, TokenType, User
from app.service.security import verify_password
from app.service.user import UserService
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

router = APIRouter(prefix="/auth")


@router.post("/register", response_model=User)
def register(payload: RegisterUserRequest, service: Annotated[UserService, Depends()]):
    if not ALLOW_REGISTER:
        raise HTTPException(status.HTTP_403_FORBIDDEN)
    user = service.find_one_by_email(payload.email)
    if user:
        raise HTTPException(status.HTTP_409_CONFLICT)
    user = service.create_user(payload.email, payload.password)
    if not user:
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR)
    return user


@router.post("/login")
def login(
    payload: Annotated[OAuth2PasswordRequestForm, Depends()],
    service: Annotated[UserService, Depends()],
):
    user = service.find_one_by_email(payload.username)
    if not user or not user.is_active:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED)
    if not verify_password(payload.password, user.password):
        raise HTTPException(status.HTTP_401_UNAUTHORIZED)
    return create_token(user.id, token_type=TokenType.BOTH)


@router.get("/me", response_model=User)
async def get_me(user: Annotated[User, Depends(get_current_active_user)]):
    return user
