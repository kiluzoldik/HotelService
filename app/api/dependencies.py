from datetime import date, datetime
from typing import Annotated

from fastapi import Depends, HTTPException, Query, Request
from pydantic import BaseModel, field_validator

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
            raise HTTPException(status_code=401, detail="Вы не предоставили токен доступа")
        return token
    
def get_current_user_id(token: str = Depends(get_token)) -> int:
    data = AuthService().decode_token(token)
    return data["user_id"]


UserIdDep = Annotated[int, Depends(get_current_user_id)]

async def get_db():
    async with DBManager(session_factory=async_session_maker) as db:
        yield db


DBDep = Annotated[DBManager, Depends(get_db)]
