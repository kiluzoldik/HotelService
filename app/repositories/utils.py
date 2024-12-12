from datetime import date
from sqlalchemy import func, select

from app.models.bookings import Bookings
from app.models.hotels import Hotels
from app.models.rooms import Rooms


async def get_room_ids_for_booking(
        date_from: date,
        date_to: date,
        hotel_id: int | None = None,
        title: str | None = None,
        location: str | None = None,
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
        
        left_table_with_hotels_fields = (
            select(
                Hotels.title,
                Hotels.location,
                rooms_left_table.c.room_id,
                rooms_left_table.c.rooms_left
            )
            .select_from(Hotels)
            .join(rooms_left_table, Hotels.id == rooms_left_table.c.hotel_id)
            .cte()
        )
        
        hotels_titles = (
            select(Hotels.title)
            .select_from(Hotels)
        )
        if title is not None:
            hotels_titles = hotels_titles.where(
                func.lower(Hotels.title)
                .contains(title.strip().lower())
            )
        hotels_titles = (
            hotels_titles
            .subquery()
        )
        
        hotels_locations = (
            select(Hotels.location)
            .select_from(Hotels)
        )
        if location is not None:
            hotels_locations = hotels_locations.where(
                func.lower(Hotels.location)
                .contains(location.strip().lower())
            )
        hotels_locations = (
            hotels_locations
            .subquery()
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
            select(left_table_with_hotels_fields.c.room_id)
            .select_from(left_table_with_hotels_fields)
            .filter(
                left_table_with_hotels_fields.c.rooms_left > 0,
                left_table_with_hotels_fields.c.room_id.in_(rooms_ids_for_hotel),
                left_table_with_hotels_fields.c.title.in_(hotels_titles),
                left_table_with_hotels_fields.c.location.in_(hotels_locations),
            )
        )
        
        return rooms_ids_to_get