from datetime import datetime

from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.sql import func
from sqlalchemy.types import UUID, DateTime, Uuid


class Base(DeclarativeBase):
    pass


class TokenEntity(Base):
    __tablename__ = "token_blacklist"

    token: Mapped[str] = mapped_column(unique=True, primary_key=True)
    expires: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, server_default=func.now()
    )


class UserEntity(Base):
    __tablename__ = "user"

    id: Mapped[UUID] = mapped_column(Uuid, primary_key=True)
    email: Mapped[str] = mapped_column(unique=True)
    password: Mapped[str]
    is_active: Mapped[bool]
    is_superuser: Mapped[bool]
