import enum
from dataclasses import dataclass
from datetime import datetime

from domain.group import Group


class RoleEnum(enum.Enum):
    user = "user"
    admin = "admin"
    moderator = "moderator"


@dataclass
class User:
    name: str
    surname: str
    username: str
    phone_number: str
    email: str
    role: RoleEnum
    group: Group

    password: str | None = None
    id: int | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None
