import enum
import re
from typing import Annotated

from pydantic import BaseModel, EmailStr, PositiveInt, StringConstraints
from pydantic.functional_validators import field_validator

from app.models import RoleEnum


class UserBase(BaseModel):
    name: str = None
    surname: str = None
    username: str = None

    phone_number: str = None
    email: EmailStr = None

    role: RoleEnum = RoleEnum.user
    group: int = None

    @field_validator("phone_number")
    @classmethod
    def is_phone_right(cls, phone: str) -> str:
        result = re.match(
            r"^[+]?[0-9]{1,4}[-\s]?\(?[0-9]{1,3}\)?[-\s]?([0-9]{1,4}[-\s]?){2}[0-9]{1,9}$",
            phone,
        )
        print(result)
        if result is None:
            raise ValueError("not valid phone")

        return phone


class GroupBase(BaseModel):
    name: str


class SortUsersFields(enum.Enum):
    name = "name"
    surname = "surname"
    username = "username"
    phone_number = "phone_number"
    email = "email"


class UsersQueryParams(BaseModel):
    page: PositiveInt | None = None
    limit: PositiveInt | None = None
    filter_by_name: str | None = None
    sort_by: SortUsersFields | None = None
    order_by: Annotated[str, StringConstraints(pattern="^(asc|desc)$")] = "asc"


class UserLogin(BaseModel):
    username: str | None = None
    phone_number: str | None = None
    email: EmailStr | None = None

    password: str = None
