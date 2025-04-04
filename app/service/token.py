from datetime import datetime, timedelta, timezone
from typing import Annotated
from uuid import UUID

import jwt

from app.config import (
    ACCESS_TOKEN_EXPIRE_MINUTES,
    ALGORITHM,
    REFRESH_TOKEN_EXPIRE_DAYS,
    SECRET_KEY,
)
from app.models import Tokens, TokenType
from app.persistence.repository.token import TokenRepository
from fastapi import Depends


def _create_token(data: dict, expires_delta: datetime):
    payload = data.copy()
    payload.update({"exp": expires_delta})
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)


def create_access_token(user_id: UUID):
    payload = {"type": "access", "sub": str(user_id)}
    expires = datetime.now(timezone.utc) + timedelta(
        minutes=ACCESS_TOKEN_EXPIRE_MINUTES
    )
    return _create_token(payload, expires)


def create_refresh_token(user_id: UUID):
    payload = {"type": "refresh", "sub": str(user_id)}
    expires = datetime.now(timezone.utc) + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    return _create_token(payload, expires)


def verify_access_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        if payload.get("type") != "access" or payload.get("sub") is None:
            return None
        return payload
    except Exception:
        return None


def verify_refresh_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        if payload.get("type") != "refresh" or payload.get("sub") is None:
            return None
        return payload
    except Exception:
        return None


class TokenService:
    def __init__(self, token_repo: Annotated[TokenRepository, Depends()]):
        self.token_repo = token_repo

    def refresh(self, token: str) -> Tokens | None:
        data = verify_refresh_token(token)
        if not data or self.token_repo.is_blacklisted(token):
            return None
        access_token = create_access_token(data.get("sub"))
        refresh_token = create_refresh_token(data.get("sub"))
        self.token_repo.add_token_to_blacklist(
            token, datetime.fromtimestamp(data.get("exp"))
        )
        return Tokens(access_token=access_token, refresh_token=refresh_token)

    def create(self, user_id, token_type: TokenType) -> Tokens:
        def __create_token(data: dict, expires_delta: datetime) -> str:
            payload = data.copy()
            payload.update({"exp": expires_delta})
            return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

        tokens = Tokens()
        if token_type == TokenType.BOTH or token_type == TokenType.ACCESS:
            payload = {"type": "access", "sub": str(user_id)}
            expires = datetime.now(timezone.utc) + timedelta(
                minutes=ACCESS_TOKEN_EXPIRE_MINUTES
            )
            tokens.access_token = __create_token(payload, expires)
        if token_type == TokenType.BOTH or token_type == TokenType.REFRESH:
            payload = {"type": "refresh", "sub": str(user_id)}
            expires = datetime.now(timezone.utc) + timedelta(
                days=REFRESH_TOKEN_EXPIRE_DAYS
            )
            tokens.refresh_token = __create_token(payload, expires)
        return tokens
