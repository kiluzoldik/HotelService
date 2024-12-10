from fastapi import APIRouter, Response, HTTPException

from app.schemas.users import AddRequestUser, AddUser
from app.services.auth import AuthService
from app.api.dependencies import UserIdDep, DBDep


router = APIRouter(prefix="/auth", tags=["Авторизация и аутентификация"])

@router.post("/register")
async def register_user(
    db: DBDep,
    data: AddRequestUser
):
    hashed_password = AuthService().hash_password(data.password)
    new_user_data = AddUser(email=data.email, hashed_password=hashed_password)
    await db.users.add(new_user_data)
    await db.commit()
            
    return {'Пользователь успешно добавлен'}
        
@router.post("/login")
async def login_user(
    db: DBDep,
    data: AddRequestUser,
    response: Response
):
    user = await db.users.get_user_with_hashed_password(data.email)
    if not user:
        raise HTTPException(status_code=401, detail="Пользователь с таким Email не зарегистрирован")
    if not AuthService().verify_password(data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Неверный пароль")
    access_token = AuthService().create_access_token({"user_id": user.id})
    response.set_cookie("access_token", access_token)
    return {"access_token": access_token}
    
@router.get("/me")
async def get_me(
    user_id: UserIdDep,
    db: DBDep
):
    user = await db.users.get_one_or_none(id=user_id)
    return user
    
@router.post("/logout")
async def logout(response: Response):
    response.delete_cookie("access_token")
    return {"status": "OK"}