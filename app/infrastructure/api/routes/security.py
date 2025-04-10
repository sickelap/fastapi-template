from typing import Annotated

from app.application.service.security import verify_password
from app.application.service.token import TokenService
from app.application.service.user import UserService
from app.config import settings
from app.domain.models import User
from app.infrastructure.api.dependencies import get_current_active_user
from app.infrastructure.models import (RefreshToken, RegisterUserRequest,
                                       Tokens, TokenType)
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

router = APIRouter(prefix="/auth")


@router.post("/register", response_model=Tokens)
async def register(
    payload: RegisterUserRequest,
    service: Annotated[UserService, Depends()],
    token_service: Annotated[TokenService, Depends()],
):
    if not settings.ALLOW_REGISTER:
        raise HTTPException(status.HTTP_403_FORBIDDEN)
    user = await service.find_one_by_email(payload.email)
    if user:
        raise HTTPException(status.HTTP_409_CONFLICT)
    user = await service.create_user(payload.email, payload.password)
    if not user:
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR)
    return token_service.create(user.id, token_type=TokenType.BOTH)


@router.post("/login", response_model=Tokens)
async def login(
    payload: Annotated[OAuth2PasswordRequestForm, Depends()],
    user_service: Annotated[UserService, Depends()],
    token_service: Annotated[TokenService, Depends()],
):
    user = await user_service.find_one_by_email(payload.username)
    if not user or not user.is_active:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED)
    if not verify_password(payload.password, user.password):
        raise HTTPException(status.HTTP_401_UNAUTHORIZED)
    return token_service.create(user.id, token_type=TokenType.BOTH)


@router.post("/refresh", response_model=Tokens)
async def refresh_token(
    payload: RefreshToken, token_service: Annotated[TokenService, Depends()]
):
    tokens = await token_service.refresh(payload.refresh_token)
    if not tokens:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED)
    return tokens


@router.get("/me", response_model=User)
async def get_me(user: Annotated[User, Depends(get_current_active_user)]):
    return user
