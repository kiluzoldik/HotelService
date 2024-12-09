from fastapi import APIRouter

from passlib.context import CryptContext

from app.schemas.users import AddRequestUser, AddUser
from app.database import async_session_maker
from app.repositories.users import UsersRepository


router = APIRouter(prefix="/auth", tags=["Авторизация и аутентификация"])

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

@router.post("/register")
async def register_user(
    data: AddRequestUser
):
    hashed_password = pwd_context.hash(data.password)
    new_user_data = AddUser(email=data.email, hashed_password=hashed_password)
    async with async_session_maker() as session:
        check_user = await UsersRepository(session).get_one_or_none(email=data.email)
        if not check_user:
            await UsersRepository(session).add(new_user_data)
            await session.commit()
            return {'Пользователь успешно добавлен'}
        
    return {"Пользователь существует"}