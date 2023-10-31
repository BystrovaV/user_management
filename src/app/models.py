import datetime
import enum

from sqlalchemy import DateTime, ForeignKey, String, create_engine
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, sessionmaker
from sqlalchemy.sql import func

from app.settings import Settings

# settings = FactorySettings(Settings().ENV_STATE)()
settings = Settings()
# engine = create_engine(f"postgresql://{settings.DB_USER}:{settings.DB_PASSWORD}@{settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_NAME}")
# engine = create_engine(settings.get_db_url)

engine = create_async_engine(
    settings.get_db_url,
    echo=True,
    future=True,
)

# Session = sessionmaker(bind=engine)
# session = Session()


class Base(DeclarativeBase):
    pass


class Group(Base):
    __tablename__ = "group"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(30))
    created_at: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )


class RoleEnum(enum.Enum):
    user = "user"
    admin = "admin"
    moderator = "moderator"


class User(Base):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(30))
    surname: Mapped[str] = mapped_column(String(30))

    username: Mapped[str] = mapped_column(String(30))

    phone_number: Mapped[str] = mapped_column(String(20))

    email: Mapped[str] = mapped_column(String(30))
    role: Mapped[RoleEnum]
    group: Mapped[int] = mapped_column(ForeignKey("group.id"))
    created_at: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )


# Base.metadata.drop_all(engine)
# Base.metadata.create_all(engine)
