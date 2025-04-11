from enum import Enum
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, EmailStr

from app.domain.models import User


class TokenType(Enum):
    ACCESS = "access"
    REFRESH = "refresh"
    BOTH = "both"


class AccessToken(BaseModel):
    access_token: str


class RefreshToken(BaseModel):
    refresh_token: str


class Tokens(BaseModel):
    access_token: Optional[str] = None
    refresh_token: Optional[str] = None


class UserInDB(User):
    password: str


class RegisterUserRequest(BaseModel):
    email: EmailStr
    password: str


class ChangePasswordRequest(BaseModel):
    old_password: str
    new_password: str


class DisableUserRequest(BaseModel):
    user_id: UUID
