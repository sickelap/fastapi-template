from datetime import datetime, timezone
from typing import Annotated

from app.infrastructure.persistence.entities import TokenEntity
from app.infrastructure.persistence.session import get_session
from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession


class TokenRepository:
    def __init__(self, session: Annotated[AsyncSession, Depends(get_session)]):
        self.session = session

    async def is_blacklisted(self, token: str):
        stmt = select(TokenEntity).where(
            TokenEntity.token == token, TokenEntity.expires > datetime.now(timezone.utc)
        )
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def add_token_to_blacklist(self, token: str, expires: datetime):
        model = TokenEntity(token=token, expires=expires)
        self.session.add(model)
        return await self.session.commit()
