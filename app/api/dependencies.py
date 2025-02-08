from typing import Annotated

from jwt.exceptions import ExpiredSignatureError
from fastapi import Depends, Query, Request
from pydantic import BaseModel

from app.exceptions import TokenNotFoundException, UserNotAuthenticatedHTTPException
from app.services.auth import AuthService
from app.database import async_session_maker
from app.utils.db_manager import DBManager


class PaginationParams(BaseModel):
    page: Annotated[int | None, Query(1, ge=1)]
    per_page: Annotated[int | None, Query(3, ge=1, le=30)]


PaginationDep = Annotated[PaginationParams, Depends()]


def get_token(request: Request) -> str:
    token = request.cookies.get("access_token", None)
    if not token:
        raise TokenNotFoundException
    return token


def get_current_user_id(token: str = Depends(get_token)) -> int:
    try:
        data = AuthService().decode_token(token)
    except ExpiredSignatureError:
        raise UserNotAuthenticatedHTTPException
    return data["user_id"]


UserIdDep = Annotated[int, Depends(get_current_user_id)]


async def get_db():
    async with DBManager(session_factory=async_session_maker) as db:
        yield db


DBDep = Annotated[DBManager, Depends(get_db)]
