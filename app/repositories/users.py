from pydantic import EmailStr

from sqlalchemy import select

from app.models.users import Users
from app.repositories.mappers.mappers import UserWithHashedPasswordDataMapper
from app.schemas.users import User
from repositories.base import BaseRepository


class UsersRepository(BaseRepository):
    model = Users
    schema = User
    
    async def get_user_with_hashed_password(self, email: EmailStr):
        query = select(self.model).filter_by(email=email)
        result = await self.session.execute(query)
        model = result.scalars().one()
        return UserWithHashedPasswordDataMapper.map_to_domain_entity(model)