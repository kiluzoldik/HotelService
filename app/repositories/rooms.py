from datetime import date

from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from app.models.rooms import Rooms
from app.repositories.mappers.mappers import (
    RoomDataMapper,
    RoomWithRelationshipDataMapper,
)
from app.repositories.utils import get_room_ids_for_booking
from app.repositories.base import BaseRepository


class RoomsRepository(BaseRepository):
    model = Rooms
    mapper = RoomDataMapper

    async def get_rooms_by_date(
        self,
        hotel_id: int,
        date_from: date,
        date_to: date,
    ):
        rooms_ids_to_get = await get_room_ids_for_booking(date_from, date_to, hotel_id)
        query = (
            select(self.model)
            .options(selectinload(self.model.facilities))
            .filter(Rooms.id.in_(rooms_ids_to_get))
        )
        result = await self.session.execute(query)
        return [
            RoomWithRelationshipDataMapper.map_to_domain_entity(object)
            for object in result.scalars().all()
        ]

    async def get_one_or_none(self, **filter_by):
        stmt = (
            select(self.model).options(selectinload(self.model.facilities)).filter_by(**filter_by)
        )
        result = await self.session.execute(stmt)
        item = result.scalars().one_or_none()
        if item is None:
            raise HTTPException(status_code=404, detail="Объект не найден")
        return RoomWithRelationshipDataMapper.map_to_domain_entity(item)
