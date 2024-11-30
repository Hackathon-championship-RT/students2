from typing import List, TYPE_CHECKING

if TYPE_CHECKING:
    from src.db.models import Result

from sqlalchemy import BigInteger, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.db.models.base import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(
        BigInteger, primary_key=True, autoincrement=True, index=True
    )
    username: Mapped[str] = mapped_column(
        String, unique=True, nullable=False, index=True
    )
    password: Mapped[str] = mapped_column(String, nullable=False)

    results: Mapped[List["Result"]] = relationship(back_populates="user", lazy="joined")
