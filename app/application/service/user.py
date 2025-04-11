from typing import Annotated
from uuid import UUID, uuid4

from fastapi import Depends
from pydantic import EmailStr

from app.application.exceptions import (
    CreateUserError,
    PasswordRulesError,
    UpdateUserError,
    UserNotFound,
)
from app.application.service.security import get_password_hash, password_rules_ok
from app.infrastructure.persistence.entities import UserEntity
from app.infrastructure.persistence.repository.user import UserRepository


class UserService:
    def __init__(self, user_repo: Annotated[UserRepository, Depends()]):
        self.user_repo = user_repo

    async def find_one_by_email(self, email: EmailStr) -> UserEntity:
        user = await self.user_repo.get_one_by(email=email)
        if not user:
            raise UserNotFound()
        return user

    async def find_one_by_id(self, user_id: UUID) -> UserEntity:
        user = await self.user_repo.get_one_by(id=user_id)
        if not user:
            raise UserNotFound()
        return user

    async def create_user(self, username: str, password: str) -> UserEntity:
        total_users = await self.user_repo.get_count()
        user = UserEntity(
            id=uuid4(),
            email=username,
            password=get_password_hash(password),
            is_active=True,
            is_superuser=total_users == 0,
        )
        user = await self.user_repo.save(user)
        if not user:
            raise CreateUserError()
        return user

    async def change_password(
        self, user_id: UUID, oldpw: str, newpw: str
    ) -> UserEntity:
        if oldpw == newpw:
            raise PasswordRulesError("old and new passwords are the same")
        if not password_rules_ok(newpw):
            raise PasswordRulesError("insecure password")
        user = await self.user_repo.get_one_by(id=user_id)
        assert user is not None
        user.password = get_password_hash(newpw)
        user = await self.user_repo.save(user)
        if not user:
            raise UpdateUserError()
        return user
