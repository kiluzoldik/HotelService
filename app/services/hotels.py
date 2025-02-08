from datetime import date
from app.exceptions import (
    HotelNotFoundException,
    ObjectNotFoundException,
    ObjectAlreadyExistsException,
    HotelAlreadyExistsException,
)
from app.schemas.hotels import Hotel, HotelAdd, UpdateHotel
from app.services.base import BaseService
from app.api.dependencies import PaginationDep


class HotelService(BaseService):
    async def get_hotels(
        self,
        pagination: PaginationDep,
        title: str | None,
        location: str | None,
        date_from: date,
        date_to: date,
    ):
        per_page = pagination.per_page
        return await self.db.hotels.get_hotels_by_date(
            title=title,
            location=location,
            date_from=date_from,
            date_to=date_to,
            limit=per_page,
            offset=(pagination.page - 1) * per_page,
        )

    async def get_hotel_by_id(self, hotel_id: int):
        return await self.db.hotels.get_one(id=hotel_id)

    async def create_hotel(self, hotel_data: HotelAdd):
        try:
            hotel = await self.db.hotels.add(hotel_data)
        except ObjectAlreadyExistsException:
            raise HotelAlreadyExistsException
        await self.db.commit()
        return hotel

    async def delete_hotel(self, hotel_id: int):
        try:
            await self.db.hotels.get_one(id=hotel_id)
        except ObjectNotFoundException:
            raise HotelNotFoundException
        await self.db.hotels.delete(id=hotel_id)
        await self.db.commit()

    async def full_update_hotel(self, hotel_id: int, hotel_data: UpdateHotel):
        try:
            await self.db.hotels.get_one(id=hotel_id)
        except ObjectNotFoundException:
            raise HotelNotFoundException
        await self.db.hotels.edit(hotel_data, id=hotel_id)
        await self.db.commit()

    async def partial_update_hotel(self, hotel_id: int, hotel_data: UpdateHotel):
        try:
            await self.db.hotels.get_one(id=hotel_id)
        except ObjectNotFoundException:
            raise HotelNotFoundException
        await self.db.hotels.edit(hotel_data, exclude_unset=True, id=hotel_id)
        await self.db.commit()

    async def get_hotel_with_check(self, hotel_id: int) -> Hotel:
        try:
            return await self.db.hotels.get_one(id=hotel_id)
        except ObjectNotFoundException as e:
            raise HotelNotFoundException from e
