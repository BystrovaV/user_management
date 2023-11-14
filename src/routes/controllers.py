import enum
import re
from typing import Annotated

from pydantic import BaseModel, EmailStr, PositiveInt, StringConstraints
from pydantic.functional_validators import field_validator, model_validator

from domain.group import Group
from domain.user import RoleEnum, User


class UserBase(BaseModel):
    name: str
    surname: str
    username: str

    phone_number: str
    email: EmailStr

    role: RoleEnum = RoleEnum.user
    group: int = None

    password: str
    repeat_password: str

    @classmethod
    @field_validator("phone_number")
    def is_phone_right(cls, phone: str) -> str:
        result = re.match(
            r"^[+]?[0-9]{1,4}[-\s]?\(?[0-9]{1,3}\)?[-\s]?([0-9]{1,4}[-\s]?){2}[0-9]{1,9}$",
            phone,
        )
        print(result)
        if result is None:
            raise ValueError("not valid phone")

        return phone

    @model_validator(mode="after")
    def check_passwords_match(self):
        pw1 = self.password
        pw2 = self.repeat_password

        if pw1 is not None and pw2 is not None and pw1 != pw2:
            raise ValueError("password do not match")

        return self

    def to_entity(self):
        return User(
            name=self.name,
            surname=self.surname,
            username=self.username,
            phone_number=self.phone_number,
            email=self.email,
            role=self.role,
            group=Group(id=self.group),
            password=self.password,
        )


class UserChange(BaseModel):
    name: str = None
    surname: str = None
    username: str = None

    phone_number: str = None
    email: EmailStr = None


class GroupBase(BaseModel):
    name: str


class SortUsersFields(enum.Enum):
    name = "name"
    surname = "surname"
    username = "username"
    phone_number = "phone_number"
    email = "email"


class UsersQueryParams(BaseModel):
    page: PositiveInt = 1
    limit: PositiveInt = 10
    filter_by_name: str | None = None
    sort_by: SortUsersFields | None = None
    order_by: Annotated[str, StringConstraints(pattern="^(asc|desc)$")] = "asc"


class UserLogin(BaseModel):
    username: str | None = None
    phone_number: str | None = None
    email: EmailStr | None = None

    password: str

    @model_validator(mode="after")
    def check_passwords_match(self):
        if self.username is None and self.phone_number is None and self.email is None:
            raise ValueError("No input")
        return self

    # def get_field(self):
    #     if self.username is not None:
    #         return {"username": self.username}
    #
    #     if self.phone_number is not None:
    #         return {"phone_number": self.username}
    #
    #     if self.email is not None:
    #         return {"email": self.username}
