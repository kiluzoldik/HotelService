from datetime import date
from sqlalchemy import select, func

from app.models.hotels import Hotels
from app.models.rooms import Rooms
from app.repositories.utils import get_room_ids_for_booking
from app.schemas.hotels import Hotel
from repositories.base import BaseRepository


class HotelsRepository(BaseRepository):
    model = Hotels
    schema = Hotel
    
    async def get_hotels_by_date(
        self,
        title: str,
        location: str,
        date_from: date,
        date_to: date,
        limit,
        offset,
    ):
        rooms_ids_to_get = await get_room_ids_for_booking(
            date_from, 
            date_to, 
            title=title, 
            location=location
        )
        hotels_ids = (
            select(Rooms.hotel_id)
            .select_from(Rooms)
            .filter(Rooms.id.in_(rooms_ids_to_get))
            .limit(limit)
            .offset(offset)
        ) 
        
        return await self.get_filtered(Hotels.id.in_(hotels_ids))