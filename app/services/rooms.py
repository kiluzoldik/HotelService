from datetime import date
from app.exceptions import (
    HotelNotFoundException,
    ObjectNotFoundException,
    RoomNotFoundException,
    check_dates,
)
from app.schemas.facilities import RoomFacilityAdd
from app.schemas.rooms import AddRoom, AddRoomRequest, Room, RoomPatch, RoomPatchRequest
from app.services.base import BaseService
from app.services.hotels import HotelService


class RoomService(BaseService):
    async def get_room_by_date(
        self,
        hotel_id: int,
        date_from: date,
        date_to: date,
    ):
        check_dates(date_from, date_to)
        return await self.db.rooms.get_rooms_by_date(hotel_id, date_from, date_to)

    async def get_room_by_id(self, hotel_id: int, room_id: int):
        await HotelService(self.db).get_hotel_with_check(hotel_id)
        await self.get_room_with_check(room_id)

    async def create_room(
        self,
        hotel_id: int,
        data: AddRoomRequest,
    ):
        _room_data = AddRoom(hotel_id=hotel_id, **data.model_dump())
        await HotelService(self.db).get_hotel_with_check(hotel_id)
        room = await self.db.rooms.add(_room_data)
        rooms_facilities_data = [
            RoomFacilityAdd(room_id=room.id, facility_id=facil_id)
            for facil_id in data.facilities_ids
        ]

        await self.db.rooms_facilities.add_bulk(rooms_facilities_data)
        await self.db.commit()
        return room

    async def full_update_room(self, hotel_id: int, room_id: int, data: AddRoomRequest):
        await HotelService(self.db).get_hotel_with_check(hotel_id)
        await self.get_room_with_check(room_id)
        _room_data = AddRoom(hotel_id=hotel_id, **data.model_dump())
        await self.db.rooms.edit(_room_data, id=room_id)
        await self.db.rooms_facilities.edit(data.facilities_ids, room_id)
        await self.db.commit()

    async def partial_update_room(self, hotel_id: int, room_id: int, data: RoomPatchRequest):
        await HotelService(self.db).get_hotel_with_check(hotel_id)
        _room_data = RoomPatch(hotel_id=hotel_id, **data.model_dump(exclude_unset=True))
        await self.get_room_with_check(room_id)
        await self.db.rooms.edit(_room_data, exclude_unset=True, id=room_id, hotel_id=hotel_id)
        await self.db.rooms_facilities.edit(
            facilities_ids=data.facilities_ids,
            room_id=room_id,
        )
        await self.db.commit()

    async def delete_room(self, hotel_id: int, room_id: int):
        await HotelService(self.db).get_hotel_with_check(hotel_id)
        await self.get_room_with_check(room_id)
        await self.db.rooms.delete(id=room_id, hotel_id=hotel_id)
        await self.db.commit()

    async def get_room_with_check(self, room_id: int) -> Room:
        try:
            return await self.db.rooms.get_one(id=room_id)
        except ObjectNotFoundException as e:
            raise RoomNotFoundException from e
