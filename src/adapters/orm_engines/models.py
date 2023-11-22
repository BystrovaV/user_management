import datetime
import uuid

import sqlalchemy
from sqlalchemy import Boolean, DateTime, ForeignKey, String, text, types
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.sql import func

from domain.user import RoleEnum


class Base(DeclarativeBase):
    pass


class GroupORM(Base):
    __tablename__ = "group"

    id: Mapped[uuid.UUID] = mapped_column(
        types.UUID, primary_key=True, server_default=text("gen_random_uuid()")
    )
    name: Mapped[str] = mapped_column(String(30))
    created_at: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )


class UserORM(Base):
    __tablename__ = "user"

    id: Mapped[uuid.UUID] = mapped_column(
        types.UUID, primary_key=True, server_default=text("gen_random_uuid()")
    )
    name: Mapped[str] = mapped_column(String(30))
    surname: Mapped[str] = mapped_column(String(30))

    username: Mapped[str] = mapped_column(String(30), unique=True)

    phone_number: Mapped[str] = mapped_column(String(20), unique=True)

    email: Mapped[str] = mapped_column(String(30), unique=True)
    role: Mapped[RoleEnum]
    group: Mapped[uuid.UUID] = mapped_column(ForeignKey("group.id"))
    created_at: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    updated_at: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    password: Mapped[str] = mapped_column(String(80), nullable=False)

    image_s3_path: Mapped[str] = mapped_column(String(200), nullable=True)
    is_blocked: Mapped[bool] = mapped_column(Boolean, server_default=sqlalchemy.false())
