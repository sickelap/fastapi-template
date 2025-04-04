from enum import Enum
from uuid import UUID

from pydantic import BaseModel, EmailStr


class TokenType(Enum):
    ACCESS = "access"
    REFRESH = "refresh"
    BOTH = "both"


class Token(BaseModel):
    pass


class AccessToken(Token):
    access_token: str


class RefreshToken(Token):
    refresh_token: str


class Tokens(AccessToken, RefreshToken):
    pass


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
