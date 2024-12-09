from app.models.users import Users
from app.schemas.users import User
from repositories.base import BaseRepository


class UsersRepository(BaseRepository):
    model = Users
    schema = User