from app.exceptions import AllRoomsAreBookedException, BookingException
from app.schemas.bookings import AddBooking, AddBookingRequest
from app.services.base import BaseService
from app.services.rooms import RoomService


class BookingService(BaseService):
    async def get_all_bookings(self):
        return await self.db.bookings.get_all()

    async def get_my_bookings(self, user_id):
        return await self.db.bookings.get_filtered(user_id=user_id)

    async def create_booking(self, user_id, data: AddBookingRequest):
        room_data = await RoomService(self.db).get_room_with_check(data.room_id)
        hotel_data = await self.db.hotels.get_one(id=room_data.hotel_id)
        _booking_data = AddBooking(user_id=user_id, price=room_data.price, **data.model_dump())
        try:
            booking_data = await self.db.bookings.add_booking(_booking_data, hotel_id=hotel_data.id)
        except BookingException:
            raise AllRoomsAreBookedException
        await self.db.commit()
        return booking_data
