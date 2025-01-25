from fastapi import APIRouter, Response

from app.exceptions import (
    IncorrectPasswordException,
    IncorrectPasswordOrEmailException,
    UserAlreadyExistsException,
    UserAlreadyExistsHTTPException,
    UserEmailNotFoundException,
    UserNotAuthenticatedException,
    UserNotAuthenticatedHTTPException,
)
from app.schemas.users import AddRequestUser
from app.services.auth import AuthService
from app.api.dependencies import UserIdDep, DBDep


router = APIRouter(prefix="/auth", tags=["Авторизация и аутентификация"])


@router.post("/register")
async def register_user(db: DBDep, data: AddRequestUser):
    try:
        await AuthService(db).register_user(data)
    except UserAlreadyExistsException as e:
        raise UserAlreadyExistsHTTPException from e
    return {"Пользователь успешно добавлен"}


@router.post("/login")
async def login_user(db: DBDep, data: AddRequestUser, response: Response):
    try:
        access_token = await AuthService(db).login_user(data, response)
    except UserEmailNotFoundException:
        raise IncorrectPasswordOrEmailException
    except IncorrectPasswordException:
        raise IncorrectPasswordOrEmailException

    return {"access_token": access_token}


@router.get("/me")
async def get_me(user_id: UserIdDep, db: DBDep):
    try:
        return await AuthService(db).get_me(user_id)
    except UserNotAuthenticatedException:
        UserNotAuthenticatedHTTPException


@router.post("/logout")
async def logout(response: Response):
    AuthService().logout(response)
    return {"status": "OK"}
