from app.models.rooms import Rooms
from repositories.base import BaseRepository


class RoomsRepository(BaseRepository):
    model = Rooms