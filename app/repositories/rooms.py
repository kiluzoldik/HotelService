from datetime import date
from sqlalchemy import func, select

from app.models.bookings import Bookings
from app.models.rooms import Rooms
from app.repositories.utils import get_room_ids_for_booking
from repositories.base import BaseRepository
from app.schemas.rooms import Room


class RoomsRepository(BaseRepository):
    model = Rooms
    schema = Room
    
    async def get_rooms_by_date(
        self,
        hotel_id: int,
        date_from: date,
        date_to: date,
    ):
        rooms_ids_to_get = await get_room_ids_for_booking(date_from, date_to, hotel_id)
        
        return await self.get_filtered(Rooms.id.in_(rooms_ids_to_get))