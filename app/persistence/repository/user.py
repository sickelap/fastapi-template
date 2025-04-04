from typing import Annotated

from sqlalchemy.orm import Session

from app.persistence.entities import UserEntity
from app.persistence.session import get_session
from fastapi import Depends


class UserRepository:
    def __init__(self, session: Annotated[Session, Depends(get_session)]):
        self.session = session

    def get_many_by(self, **kwargs):
        return self.session.query(UserEntity).filter_by(**kwargs)

    def get_one_by(self, **kwargs) -> UserEntity | None:
        return self.session.query(UserEntity).filter_by(**kwargs).first()

    def get_count(self):
        return self.session.query(UserEntity).count()

    def save(self, user: UserEntity):
        try:
            self.session.add(user)
            self.session.commit()
            self.session.refresh(user)
            return user
        except Exception:
            return None
