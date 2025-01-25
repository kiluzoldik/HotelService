from fastapi import APIRouter, Body

from app.exceptions import AllRoomsAreBookedException, AllRoomsAreBookedHTTPException
from app.schemas.bookings import AddBookingRequest
from app.api.dependencies import DBDep, UserIdDep
from app.services.bookings import BookingService


router = APIRouter(prefix="/bookings", tags=["Бронирование"])


@router.get(
    "",
    summary="Получение всех бронирований",
    description="<h1>Получение всех бронирований (можно получить без аутентификации)</h1>",
)
async def get_all_bookings(db: DBDep):
    return await BookingService(db).get_all_bookings()


@router.get("/me", summary="Получение бронирований текущего пользователя")
async def get_my_bookings(user_id: UserIdDep, db: DBDep):
    return await BookingService(db).get_my_bookings(user_id=user_id)


@router.post("")
async def create_booking(
    user_id: UserIdDep,
    db: DBDep,
    data: AddBookingRequest = Body(
        openapi_examples={
            "1": {
                "summary": "Создание бронирования",
                "value": {
                    "room_id": "5",
                    "date_from": "2025-01-01",
                    "date_to": "2025-02-01",
                },
            }
        }
    ),
):
    try:
        booking_data = await BookingService(db).create_booking(user_id, data)
    except AllRoomsAreBookedException:
        raise AllRoomsAreBookedHTTPException
    return {"status": "OK", "data": booking_data}
