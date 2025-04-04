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


def create_access_token(user_id: UUID):
    expires = datetime.now(timezone.utc) + timedelta(
        minutes=ACCESS_TOKEN_EXPIRE_MINUTES
    )
    payload = {"type": "access", "sub": str(user_id), "exp": expires}
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)


def create_refresh_token(user_id: UUID):
    expires = datetime.now(timezone.utc) + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    payload = {"type": "refresh", "sub": str(user_id), "exp": expires}
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)


def verify_access_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        if payload.get("type") != "access" or payload.get("sub") is None:
            return None
        return payload
    except jwt.InvalidTokenError:
        return None


def verify_refresh_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        if payload.get("type") != "refresh" or payload.get("sub") is None:
            return None
        return payload
    except jwt.InvalidTokenError:
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
        tokens = Tokens()
        if token_type == TokenType.BOTH or token_type == TokenType.ACCESS:
            tokens.access_token = create_access_token(user_id)
        if token_type == TokenType.BOTH or token_type == TokenType.REFRESH:
            tokens.refresh_token = create_refresh_token(user_id)
        return tokens
