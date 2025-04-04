import uuid
from datetime import datetime, timedelta, timezone
from typing import Annotated

import jwt

from app.config import (
    ACCESS_TOKEN_EXPIRE_MINUTES,
    ALGORITHM,
    REFRESH_TOKEN_EXPIRE_DAYS,
    SECRET_KEY,
)
from app.models import TokenType, User, UserInDB
from app.service.user import UserService
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/token")


def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)],
    user_service: Annotated[UserService, Depends()],
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("sub")
        if user_id is None:
            raise credentials_exception
    except Exception:
        raise credentials_exception
    user = user_service.find_one_by_id(uuid.UUID(user_id))
    if user is None:
        raise credentials_exception
    return user


def get_current_active_user(
    user: Annotated[UserInDB, Depends(get_current_user)],
) -> User | None:
    if not user.is_active:
        return None
    return user


def create_token(user_id, token_type: TokenType):
    def __create_token(data: dict, expires_delta: datetime) -> str:
        payload = data.copy()
        payload.update({"exp": expires_delta})
        return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

    tokens = dict()
    if token_type == TokenType.BOTH or token_type == TokenType.ACCESS:
        payload = {"type": "access", "sub": str(user_id)}
        expires = datetime.now(timezone.utc) + timedelta(
            minutes=ACCESS_TOKEN_EXPIRE_MINUTES
        )
        tokens["access_token"] = __create_token(payload, expires)
    if token_type == TokenType.BOTH or token_type == TokenType.REFRESH:
        payload = {"type": "refresh", "sub": str(user_id)}
        expires = datetime.now(timezone.utc) + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
        tokens["refresh_token"] = __create_token(payload, expires)
    return tokens
