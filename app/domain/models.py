from uuid import UUID

from pydantic import BaseModel, EmailStr


class User(BaseModel):
    id: UUID
    email: EmailStr
    is_active: bool
    is_superuser: bool
