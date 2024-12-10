from sqlalchemy import select

from app.models.rooms import Rooms
from repositories.base import BaseRepository
from app.schemas.rooms import Room


class RoomsRepository(BaseRepository):
    model = Rooms
    schema = Room
    
    async def get_all(self, hotel_id: int) -> list[Room]:
        query = select(self.model).filter_by(hotel_id=hotel_id)
        result = await self.session.execute(query)
        return [self.schema.model_validate(
            object,
            from_attributes=True
        ) for object in result.scalars().all()]