from datetime import date
from app.schemas.bookings import AddBooking


async def test_booking_crud(db):
    room_id = (await db.rooms.get_all())[0].id
    user_id = (await db.users.get_all())[0].id
    booking_data = AddBooking(
        room_id=room_id,
        user_id=user_id,
        date_from=date(year=2025, month=1, day=24),
        date_to=date(year=2025, month=1, day=17),
        price=2700,
    )
    await db.bookings.add(booking_data)
    
    booking = await db.bookings.get_one_or_none(id=1)
    assert booking
    
    updated_booking_data = AddBooking(
        room_id=2,
        user_id=user_id,
        date_from=date(year=2025, month=2, day=19),
        date_to=date(year=2025, month=2, day=9),
        price=5000,
    )
    await db.bookings.edit(updated_booking_data, exclude_unset=True, id=1)
    
    await db.bookings.delete(id=1)
    
    await db.commit()