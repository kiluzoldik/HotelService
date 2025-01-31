from datetime import date
from fastapi import APIRouter, Body

from app.exceptions import (
    DatefromIsLaterThanDatetoException,
    HotelNotFoundException,
    HotelNotFoundHTTPException,
    ObjectNotFoundException,
    RoomNotFoundHTTPException,
    ViolatesFKException,
    check_dates,
)
from app.schemas.facilities import RoomFacilityAdd
from app.schemas.rooms import (
    AddRoom,
    RoomPatchRequest,
    AddRoomRequest,
    RoomPatch,
    RoomWithRelationship,
)
from app.api.dependencies import DBDep
from app.services.rooms import RoomService


router = APIRouter(prefix="/hotels", tags=["Номера"])


@router.get(
    "/{hotel_id}/rooms",
    summary="Получение всех свободных номеров",
)
async def get_rooms(
    hotel_id: int,
    db: DBDep,
    date_from: date,
    date_to: date,
) -> list[RoomWithRelationship]:
    result = await RoomService(db).get_room_by_date(
        hotel_id=hotel_id,
        date_from=date_from,
        date_to=date_to,
    )
    return result


@router.get(
    "/{hotel_id}/rooms/{room_id}",
    summary="Получение номера",
    description="<h1>Получение конкретного номера по его идентификатору (id)</h1>",
)
async def get_room_by_id(hotel_id: int, room_id: int, db: DBDep):
    return await RoomService(db).get_room_by_id(hotel_id=hotel_id, room_id=room_id)


@router.post(
    "/{hotel_id}/rooms",
    summary="Создание номера",
    description="<h1>Создание номера отеля</h1>",
)
async def create_room(
    hotel_id: int,
    db: DBDep,
    data: AddRoomRequest = Body(
        openapi_examples={
            "1": {
                "summary": "Пример создания номера отеля",
                "value": {
                    "title": "Номер 1",
                    "description": "Описание номера",
                    "price": 2000,
                    "quantity": 10,
                    "facilities_ids": [],
                },
            }
        }
    ),
):
    try:
        room = await RoomService(db).create_room(hotel_id=hotel_id, data=data)
    except HotelNotFoundException:
        raise HotelNotFoundHTTPException
    return {"status": "OK", "data": room}


@router.put(
    "/{hotel_id}/rooms/{room_id}",
    summary="Полное изменение номера",
    description="<h1>Полное изменение номера отеля по его идентификатору (id)</h1>",
)
async def full_update_room(hotel_id: int, room_id: int, db: DBDep, data: AddRoomRequest = Body()):
    await RoomService(db).full_update_room(hotel_id=hotel_id, room_id=room_id, data=data)
    return {"status": "OK"}


@router.patch(
    "/{hotel_id}/rooms/{room_id}",
    summary="Частичное изменение номера",
    description="<h1>Частичное изменение номера отеля по его идентификатору (id)</h1>",
)
async def partial_update_room(
    hotel_id: int, room_id: int, db: DBDep, data: RoomPatchRequest = Body()
):
    await RoomService(db).partial_update_room(hotel_id=hotel_id, room_id=room_id, data=data)
    return {"status": "OK"}


@router.delete(
    "/{hotel_id}/rooms/{room_id}",
    summary="Удаление номера",
    description="<h1>Удаление номера отеля по его идентификатору (id)</h1>",
)
async def delete_room(hotel_id: int, room_id: int, db: DBDep):
    await RoomService(db).delete_room(hotel_id=hotel_id, room_id=room_id)
    return {"status": "OK"}
