from sqlalchemy import delete, insert

from app.models.facilities import Facilities, RoomsFacilities
from app.repositories.base import BaseRepository
from app.schemas.facilities import Facility, RoomFacility


class FacilitiesRepository(BaseRepository):
    model = Facilities
    schema = Facility
    

class RoomsFacilitiesRepository(BaseRepository):
    model = RoomsFacilities
    schema = RoomFacility
    
    async def edit(
        self, 
        facilities_ids: list[int], 
        room_id: int,
    ):
        db_data = await self.get_filtered(room_id=room_id)
        delete_stmt = (
            delete(self.model)
            .where(
                self.model.room_id == room_id,
                self.model.facility_id.notin_(facilities_ids)
            )
        )
        await self.session.execute(delete_stmt)
        
        set_facilities = {item.facility_id for item in db_data}
        to_add = set(facilities_ids) - set_facilities
        add_stmt = (
            insert(self.model)
            .values([{"room_id": room_id, "facility_id": _id} for _id in to_add])
        )
        await self.session.execute(add_stmt)
        