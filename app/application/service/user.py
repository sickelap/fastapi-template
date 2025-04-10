from typing import Annotated
from uuid import UUID, uuid4

from fastapi import Depends
from pydantic import EmailStr

from app.application.service.security import get_password_hash
from app.infrastructure.persistence.entities import UserEntity
from app.infrastructure.persistence.repository.user import UserRepository


class UserService:
    def __init__(self, user_repo: Annotated[UserRepository, Depends()]):
        self.user_repo = user_repo

    async def find_one_by_email(self, email: EmailStr) -> UserEntity | None:
        return await self.user_repo.get_one_by(email=email)

    async def find_one_by_id(self, user_id: UUID) -> UserEntity | None:
        return await self.user_repo.get_one_by(id=user_id)

    async def create_user(self, username: str, password: str) -> UserEntity | None:
        total_users = await self.user_repo.get_count()
        user = UserEntity(
            id=uuid4(),
            email=username,
            password=get_password_hash(password),
            is_active=True,
            is_superuser=total_users == 0,
        )
        return await self.user_repo.save(user)
