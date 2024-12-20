from datetime import date
from sqlalchemy import func, select

from app.models.hotels import Hotels
from app.models.rooms import Rooms
from app.repositories.mappers.mappers import HotelDataMapper
from app.repositories.utils import get_room_ids_for_booking
from app.repositories.base import BaseRepository


class HotelsRepository(BaseRepository):
    model = Hotels
    mapper = HotelDataMapper
    
    async def get_hotels_by_date(
        self,
        title: str,
        location: str,
        date_from: date,
        date_to: date,
        limit,
        offset,
    ):
        rooms_ids_to_get = await get_room_ids_for_booking(date_from, date_to)
        hotels_ids = (
            select(Rooms.hotel_id)
            .select_from(Rooms)
            .filter(Rooms.id.in_(rooms_ids_to_get))
        ) 
        
        query = select(Hotels).filter(Hotels.id.in_(hotels_ids))
        if location:
            query = query.filter(func.lower(Hotels.location).contains(location.strip().lower()))
        if title:
            query = query.filter(func.lower(Hotels.title).contains(title.strip().lower()))
        query = (
            query
            .limit(limit)
            .offset(offset)
        )
        result = await self.session.execute(query)

        return [self.mapper.map_to_domain_entity(hotel) for hotel in result.scalars().all()]