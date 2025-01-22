from datetime import date
from fastapi import APIRouter, Body, HTTPException

from app.exceptions import DatefromIsLaterThanDatetoException, ObjectNotFoundException, ViolatesFKException
from app.schemas.facilities import RoomFacilityAdd
from app.schemas.rooms import (
    AddRoom,
    RoomPatchRequest,
    AddRoomRequest,
    RoomPatch,
    RoomWithRelationship,
)
from app.api.dependencies import DBDep


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
    try:
        result = await db.rooms.get_rooms_by_date(hotel_id, date_from, date_to)
    except DatefromIsLaterThanDatetoException as e:
        raise HTTPException(status_code=422, detail=e.detail)
    
    return result


@router.get(
    "/{hotel_id}/rooms/{room_id}",
    summary="Получение номера",
    description="<h1>Получение конкретного номера по его идентификатору (id)</h1>",
)
async def get_room_by_id(hotel_id: int, room_id: int, db: DBDep):
    try:
        result = await db.rooms.get_one(id=room_id, hotel_id=hotel_id)
    except ObjectNotFoundException:
        raise HTTPException(status_code=404, detail="Номер не найден")
        
    return result


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
                    "facilities_ids": [2, 3],
                },
            }
        }
    ),
):
    _room_data = AddRoom(hotel_id=hotel_id, **data.model_dump())
    try:
        await db.hotels.get_one(id=hotel_id)
    except ObjectNotFoundException:
        raise HTTPException(status_code=404, detail="Отель не найден")
    room = await db.rooms.add(_room_data)
    rooms_facilities_data = [
        RoomFacilityAdd(room_id=room.id, facility_id=facil_id) for facil_id in data.facilities_ids
    ]

    await db.rooms_facilities.add_bulk(rooms_facilities_data)
    await db.commit()

    return {"status": "OK", "data": room}


@router.put(
    "/{hotel_id}/rooms/{room_id}",
    summary="Полное изменение номера",
    description="<h1>Полное изменение номера отеля по его идентификатору (id)</h1>",
)
async def full_update_room(hotel_id: int, room_id: int, db: DBDep, data: AddRoomRequest = Body()):
    try:
        await db.hotels.get_one(id=hotel_id)
    except ObjectNotFoundException:
        raise HTTPException(status_code=404, detail="Отель не найден")
    
    _room_data = AddRoom(hotel_id=hotel_id, **data.model_dump())
    
    try:
        await db.rooms.edit(_room_data, id=room_id)
        await db.rooms_facilities.edit(data.facilities_ids, room_id)
    except (ObjectNotFoundException, ViolatesFKException):
        raise HTTPException(status_code=404, detail="Номер не найден")
    
    await db.commit()
    
    return {"status": "OK"}


@router.patch(
    "/{hotel_id}/rooms/{room_id}",
    summary="Частичное изменение номера",
    description="<h1>Частичное изменение номера отеля по его идентификатору (id)</h1>",
)
async def partial_update_room(
    hotel_id: int, room_id: int, db: DBDep, data: RoomPatchRequest = Body()
):
    try:
        await db.hotels.get_one(id=hotel_id)
    except ObjectNotFoundException:
        raise HTTPException(status_code=404, detail="Отель не найден")
    
    _room_data = RoomPatch(hotel_id=hotel_id, **data.model_dump(exclude_unset=True))
    
    try:
        await db.rooms.get_one(id=room_id)
    except ObjectNotFoundException:
        raise HTTPException(status_code=404, detail="Номер не найден")
    
    await db.rooms.edit(_room_data, exclude_unset=True, id=room_id, hotel_id=hotel_id)
    await db.rooms_facilities.edit(
        facilities_ids=data.facilities_ids,
        room_id=room_id,
    )
    await db.commit()
    
    return {"status": "OK"}


@router.delete(
    "/{hotel_id}/rooms/{room_id}",
    summary="Удаление номера",
    description="<h1>Удаление номера отеля по его идентификатору (id)</h1>",
)
async def delete_room(hotel_id: int, room_id: int, db: DBDep):
    try:
        await db.hotels.get_one(id=hotel_id)
    except ObjectNotFoundException:
        raise HTTPException(status_code=404, detail="Отель не найден")
    
    try:
        await db.rooms.delete(id=room_id, hotel_id=hotel_id)
    except ObjectNotFoundException:
        raise HTTPException(status_code=404, detail="Номер не найден")
    
    await db.commit()
    
    return {"status": "OK"}
