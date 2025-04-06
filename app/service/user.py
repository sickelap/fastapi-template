from typing import Annotated
from uuid import UUID

from pydantic import EmailStr

from app.persistence.entities import UserEntity
from app.persistence.repository.user import UserRepository
from app.service.security import get_password_hash
from fastapi import Depends


class UserService:
    def __init__(self, user_repo: Annotated[UserRepository, Depends()]):
        self.user_repo = user_repo

    def find_one_by_email(self, email: EmailStr) -> UserEntity | None:
        return self.user_repo.get_one_by(email=email)

    def find_one_by_id(self, user_id: UUID) -> UserEntity | None:
        return self.user_repo.get_one_by(id=user_id)

    def create_user(self, username: str, password: str) -> UserEntity | None:
        total_users = self.user_repo.get_count()
        user = UserEntity(
            email=username,
            password=get_password_hash(password),
            is_active=True,
            is_superuser=total_users == 0,
        )
        return self.user_repo.save(user)
