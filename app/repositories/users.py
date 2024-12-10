from pydantic import EmailStr

from sqlalchemy import select

from app.models.users import Users
from app.schemas.users import User, UserWithHashedPassword
from repositories.base import BaseRepository


class UsersRepository(BaseRepository):
    model = Users
    schema = User
    
    async def get_user_with_hashed_password(self, email: EmailStr):
        query = select(self.model).filter_by(email=email)
        result = await self.session.execute(query)
        model = result.scalars().one()
        return UserWithHashedPassword.model_validate(model, from_attributes=True)