from fastapi import APIRouter, Body

from app.schemas.bookings import AddBooking, AddBookingRequest
from app.api.dependencies import DBDep, UserIdDep


router = APIRouter(
    prefix="/bookings",
    tags=["Бронирование"]
)

@router.post("")
async def create_booking(
    user_id: UserIdDep, 
    db: DBDep, 
    data: AddBookingRequest = Body(openapi_examples={
    "1": {
        "summary": "Создание бронирования",
        "value": {
            "room_id": "5",
            "date_from": "2025-01-01",
            "date_to": "2025-02-01"
        }
    }
})
):
    room_data = await db.rooms.get_one_or_none(id=data.room_id)
    _booking_data = AddBooking(
        user_id=user_id,
        price=room_data.price,
        **data.model_dump()
    )
    await db.bookings.add(_booking_data)
    await db.commit()
    return {"status": "OK", "data": _booking_data}