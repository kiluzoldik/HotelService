from datetime import date
from sqlalchemy import func, select

from app.models.bookings import Bookings
from app.models.rooms import Rooms


async def get_room_ids_for_booking(
        date_from: date,
        date_to: date,
        hotel_id: int | None = None,
    ):
        rooms_count = (
            select(Bookings.room_id, func.count("*").label("rooms_booked"))
            .select_from(Bookings)
            .filter(
                Bookings.date_to >= date_from,
                Bookings.date_from <= date_to,
            )
            .group_by(Bookings.room_id)
            .cte(name="rooms_count")
        )
        
        rooms_left_table = (
            select(
                Rooms.hotel_id,
                Rooms.id.label("room_id"),
                (Rooms.quantity - func.coalesce(rooms_count.c.rooms_booked, 0)).label("rooms_left") 
            )
            .select_from(Rooms)
            .outerjoin(rooms_count, Rooms.id == rooms_count.c.room_id)
            .cte(name="rooms_left_table")
        )
        
        rooms_ids_for_hotel = (
            select(Rooms.id)
            .select_from(Rooms)
        )
        if hotel_id is not None:
            rooms_ids_for_hotel = rooms_ids_for_hotel.filter(Rooms.hotel_id == hotel_id)
        
        rooms_ids_for_hotel = (
            rooms_ids_for_hotel
            .subquery()
        )
        
        rooms_ids_to_get = (
            select(rooms_left_table.c.room_id)
            .select_from(rooms_left_table)
            .filter(
                rooms_left_table.c.rooms_left > 0,
                rooms_left_table.c.room_id.in_(rooms_ids_for_hotel),
            )
        )
        
        return rooms_ids_to_get