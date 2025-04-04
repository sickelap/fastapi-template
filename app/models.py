from enum import Enum
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, EmailStr


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


class User(BaseModel):
    id: UUID
    email: EmailStr


class UserInDB(User):
    password: str
    is_active: bool
    is_superuser: bool


class RegisterUserRequest(BaseModel):
    email: EmailStr
    password: str
