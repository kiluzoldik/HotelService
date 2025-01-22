from pydantic import BaseModel, EmailStr


class AddRequestUser(BaseModel):
    email: EmailStr
    password: str


class AddUser(BaseModel):
    email: EmailStr
    hashed_password: str


class User(BaseModel):
    id: int
    email: EmailStr


class UserWithHashedPassword(User):
    hashed_password: str
