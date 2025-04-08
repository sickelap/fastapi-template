from typing import Annotated

from app.persistence.entities import UserEntity
from app.persistence.session import get_session
from fastapi import Depends
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession


class UserRepository:
    def __init__(self, session: Annotated[AsyncSession, Depends(get_session)]):
        self.session = session

    async def get_one_by(self, **kwargs) -> UserEntity | None:
        stmt = select(UserEntity).filter_by(**kwargs)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def get_count(self):
        stmt = select(func.count()).select_from(UserEntity)
        result = await self.session.execute(stmt)
        return result.scalar_one()

    async def save(self, user: UserEntity):
        try:
            self.session.add(user)
            await self.session.commit()
            await self.session.refresh(user)
            return user
        except Exception:
            return None
