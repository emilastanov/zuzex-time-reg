from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import Enum, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship, backref
from sqlalchemy.sql import func

from .base import Base, CRUDMixin

if TYPE_CHECKING:
    from models.User import User


class ZuzexProfile(Base, CRUDMixin):
    __tablename__ = "zuzex_profiles"

    id: Mapped[int] = mapped_column(primary_key=True)

    hashed_auth_key: Mapped[str] = mapped_column(nullable=False)
    task_key: Mapped[str] = mapped_column(nullable=False)

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)

    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        server_default=func.now(), onupdate=func.now()
    )

    user: Mapped["User"] = relationship(
        backref=backref("zuzex_profiles", uselist=True), foreign_keys=[user_id]
    )
