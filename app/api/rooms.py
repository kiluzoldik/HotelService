from fastapi import APIRouter, Body

from app.schemas.rooms import Room, AddRoom, UpdateRoom
from app.database import async_session_maker
from app.repositories.rooms import RoomsRepository


router = APIRouter(prefix="/hotels/{hotel_id}", tags=["Номера"])


@router.get(
    "/rooms", 
    response_model=list[Room],
    summary="Получение всех номеров",
    description="<h1>Получение ВСЕХ номеров ВСЕХ отелей</h1>"
)
async def get_rooms(hotel_id: int) -> list[Room]:
    async with async_session_maker() as session:
        return await RoomsRepository(session).get_all(hotel_id)
        
    
@router.get(
    "/rooms/{room_id}",
    summary="Получение номера",
    description="<h1>Получение конкретного номера по его идентификатору (id)</h1>"
)
async def get_room_by_id(room_id: int):
    async with async_session_maker() as session:
        return await RoomsRepository(session).get_one_or_none(id=room_id)
    
@router.post(
    "/rooms",
    summary="Создание номера",
    description="<h1>Создание номера отеля</h1>"
)
async def create_room(data: AddRoom = Body(openapi_examples={
    "1": {
        "summary": "Пример создания номера отеля",
        "value": {
            "hotel_id": 1,
            "title": "Номер 1",
            "description": "Описание номера",
            "price": 2000,
            "quantity": 10
        }
    }
})
):
    async with async_session_maker() as session:
        room = await RoomsRepository(session).add(data)
        await session.commit()
        return room
    
@router.put(
    "/rooms/{room_id}",
    summary="Полное изменение номера",
    description="<h1>Полное изменение номера отеля по его идентификатору (id)</h1>"
)
async def full_update_room(room_id: int, data: UpdateRoom):
    async with async_session_maker() as session:
        await RoomsRepository(session).edit(data, id=room_id)
        await session.commit()
    
    return {"status": "OK"}
    
@router.patch(
    "/rooms/{room_id}",
    summary="Частичное изменение номера",
    description="<h1>Частичное изменение номера отеля по его идентификатору (id)</h1>"
)
async def partial_update_room(room_id: int, data: UpdateRoom):
    async with async_session_maker() as session:
        await RoomsRepository(session).edit(data, exclude_unset=True, id=room_id)
        await session.commit()
        
    return {"status": "OK"}
    
@router.delete(
    "/rooms/{room_id}",
    summary="Удаление номера",
    description="<h1>Удаление номера отеля по его идентификатору (id)</h1>"
)
async def delete_room(room_id: int):
    async with async_session_maker() as session:
        await RoomsRepository(session).delete(id=room_id)
        await session.commit()
        
    return {"status": "OK"}