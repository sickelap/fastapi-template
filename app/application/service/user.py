from typing import Annotated
from uuid import UUID, uuid4

from fastapi import Depends
from pydantic import EmailStr

from app.application.service.security import get_password_hash, password_rules_ok
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

    async def change_password(
        self, user_id: UUID, old_password: str, new_password: str
    ):
        user = await self.user_repo.get_one_by(id=user_id)
        if not user:
            raise Exception("unable to find user")
        if old_password == new_password:
            raise Exception("old and new passwords are the same")
        if not password_rules_ok(new_password):
            raise Exception("insecure password")
        user.password = get_password_hash(new_password)
        return await self.user_repo.save(user)
