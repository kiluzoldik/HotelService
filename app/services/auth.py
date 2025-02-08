from datetime import datetime, timedelta, timezone

from fastapi import Response
from passlib.context import CryptContext
from sqlalchemy.exc import NoResultFound
from validate_email_address import validate_email
import jwt

from app.config import settings
from app.exceptions import (
    EmailException,
    IncorrectPasswordException,
    IncorrectTokenException,
    ObjectAlreadyExistsException,
    UserAlreadyExistsException,
    UserEmailNotFoundException,
    UserNotAuthenticatedException,
)
from app.schemas.users import AddRequestUser, AddUser
from app.services.base import BaseService


class AuthService(BaseService):
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    def verify_password(self, password, hashed_password):
        return self.pwd_context.verify(password, hashed_password)

    def create_access_token(self, data: dict) -> str:
        to_encode = data.copy()
        expire = datetime.now(timezone.utc) + timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(
            to_encode, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM
        )
        return encoded_jwt

    def hash_password(self, password: str) -> str:
        return self.pwd_context.hash(password)

    def get_password_hash(self, password):
        return self.pwd_context.hash(password)

    def decode_token(self, token: str) -> str:
        try:
            return jwt.decode(
                token, key=settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM]
            )
        except jwt.exceptions.DecodeError:
            raise IncorrectTokenException

    async def register_user(self, data: AddRequestUser):
        is_valid = validate_email(data.email, verify=True)
        if not is_valid:
            raise EmailException
        hashed_password = AuthService().hash_password(data.password)
        new_user_data = AddUser(email=data.email, hashed_password=hashed_password)
        try:
            await self.db.users.add(new_user_data)
        except ObjectAlreadyExistsException as e:
            raise UserAlreadyExistsException from e
        await self.db.commit()

    async def login_user(self, data: AddRequestUser, response: Response):
        try:
            user = await self.db.users.get_user_with_hashed_password(data.email)
        except NoResultFound:
            raise UserEmailNotFoundException
        if not self.verify_password(data.password, user.hashed_password):
            raise IncorrectPasswordException
        access_token = AuthService().create_access_token({"user_id": user.id})
        response.set_cookie("access_token", access_token)
        return access_token

    async def get_me(self, user_id):
        user = await self.db.users.get_one_or_none(id=user_id)
        if not user:
            raise UserNotAuthenticatedException
        return user

    def logout(self, response: Response):
        response.delete_cookie("access_token")
