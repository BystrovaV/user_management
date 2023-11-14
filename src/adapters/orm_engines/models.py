import datetime
import enum

from sqlalchemy import DateTime, ForeignKey, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.sql import func

from domain.user import RoleEnum


class Base(DeclarativeBase):
    pass


class GroupORM(Base):
    __tablename__ = "group"

    id: Mapped[int] = mapped_column(autoincrement=True, primary_key=True)
    name: Mapped[str] = mapped_column(String(30))
    created_at: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )


# class RoleEnum(enum.Enum):
#     user = "user"
#     admin = "admin"
#     moderator = "moderator"


class UserORM(Base):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(autoincrement=True, primary_key=True)
    name: Mapped[str] = mapped_column(String(30))
    surname: Mapped[str] = mapped_column(String(30))

    username: Mapped[str] = mapped_column(String(30), unique=True)

    phone_number: Mapped[str] = mapped_column(String(20), unique=True)

    email: Mapped[str] = mapped_column(String(30), unique=True)
    role: Mapped[RoleEnum]
    group: Mapped[int] = mapped_column(ForeignKey("group.id"))
    created_at: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    updated_at: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    password: Mapped[str] = mapped_column(String(80), nullable=False)
