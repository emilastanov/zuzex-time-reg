from datetime import datetime

from sqlalchemy import Enum
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import func
from enum import Enum as EnumBase

from .base import Base, CRUDMixin


class UserType(EnumBase):
    supergroup = "supergroup"
    channel = "channel"
    private = "private"
    group = "group"


class User(Base, CRUDMixin):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)

    chat_id: Mapped[int] = mapped_column(unique=True, nullable=False)
    chat_type: Mapped[UserType] = mapped_column(
        Enum(UserType, name="user_type_enum"), nullable=False
    )
    language_code: Mapped[str] = mapped_column(nullable=True)
    group_title: Mapped[str] = mapped_column(nullable=True)
    first_name: Mapped[str] = mapped_column(nullable=True)
    last_name: Mapped[str] = mapped_column(nullable=True)
    username: Mapped[str] = mapped_column(nullable=True)

    is_active: Mapped[bool] = mapped_column(server_default="1", nullable=False)
    is_admin: Mapped[bool] = mapped_column(server_default="0", nullable=False)

    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        server_default=func.now(), onupdate=func.now()
    )
