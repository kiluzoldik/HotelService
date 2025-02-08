from pydantic import BaseModel, field_validator

from app.exceptions import (
    DigitPasswordHTTPException,
    LengthPasswordHTTPException,
    SpecialSimbolPasswordHTTPException,
    UpperLetterPasswordHTTPException,
)


class AddRequestUser(BaseModel):
    email: str
    password: str

    @field_validator("password")
    @classmethod
    def validate_password(cls, value: str):
        if len(value) < 8:
            raise LengthPasswordHTTPException
        if not any(c.isdigit() for c in value):
            raise DigitPasswordHTTPException
        if not any(c.isupper() for c in value):
            raise UpperLetterPasswordHTTPException
        if not any(c in "!@#$%^&*()-_=+[]{};:,.<>?/|" for c in value):
            raise SpecialSimbolPasswordHTTPException
        return value


class AddUser(BaseModel):
    email: str
    hashed_password: str


class User(BaseModel):
    id: int
    email: str


class UserWithHashedPassword(User):
    hashed_password: str
