from datetime import datetime, timezone
from typing import Annotated

from sqlalchemy import select

from app.persistence.entities import TokenEntity
from app.persistence.session import Session, get_session
from fastapi import Depends


class TokenRepository:
    def __init__(self, session: Annotated[Session, Depends(get_session)]):
        self.session = session

    def is_blacklisted(self, token: str):
        stmt = select(TokenEntity).where(
            TokenEntity.token == token, TokenEntity.expires > datetime.now(timezone.utc)
        )
        return self.session.execute(stmt).first()

    def add_token_to_blacklist(self, token: str, expires: datetime):
        model = TokenEntity(token=token, expires=expires)
        self.session.add(model)
        self.session.commit()
