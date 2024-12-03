from typing import Annotated
from fastapi import Form, APIRouter, Query

from app.schemas.hotels import Hotel, UpdateHotel
from app.api.dependencies import PaginationDep


router = APIRouter(
    prefix="/hotels",
    tags=["Отели"],
)


hotels = [
    {"id": 1, "title": "Hotel A", "name": "sochi"},
    {"id": 2, "title": "Hotel B", "name": "moscow"},
    {"id": 3, "title": "Мальдивы", "name": "maldivi"},
    {"id": 4, "title": "Геленджик", "name": "gelendzhik"},
    {"id": 5, "title": "Москва", "name": "moscow"},
    {"id": 6, "title": "Казань", "name": "kazan"},
    {"id": 7, "title": "Санкт-Петербург", "name": "spb"},
]


@router.get(
    "", 
    summary="Получить список всех отелей",
    description="<h1>Получить список всех отелей с их id, названиями и городами</h1>",
)
async def get_hotels(pagination: PaginationDep):
    start = (pagination.page - 1) * pagination.per_page
    return hotels[start:start + pagination.per_page]


@router.get(
    "/{hotel_id}", 
    summary="Получить отель по ID",
    description="<h1>Получить отель по его ID с его id, названием и городом</h1>",
)
async def get_hotel(hotel_id: int):
    return [hotel for hotel in hotels if hotel["id"] == hotel_id]


@router.post(
    "", 
    summary="Создать новый отель",
    description="<h1>Создать новый отель с его названием и городом</h1>",
)
async def create_hotel(hotel_data: Hotel):
    hotels.append({"id": hotels[-1]["id"] + 1, "title": hotel_data.title, "name": hotel_data.name})
    return {"message": "Отель успешно добавлен"}


@router.delete(
    "/{hotel_id}", 
    summary="Удалить отель по ID",
    description="<h1>Удалить отель по его ID</h1>",
)
async def delete_hotel(hotel_id: int):
    global hotels
    hotels = [hotel for hotel in hotels if hotel["id"] != hotel_id]
    return {"message": "Отель успешно удален"}


@router.put(
    "/{hotel_id}", 
    summary="Изменить отель полностью по ID",
    description="<h1>Изменить отель полностью по его ID с его новыми названием и городом</h1>",
)
async def full_update_hotel(hotel_id: int, hotel_data: UpdateHotel):
    for hotel in hotels:
        if hotel["id"] == hotel_id:
            hotel["title"] = hotel_data.title
            hotel["name"] = hotel_data.name
            return {"message": "Отель успешно изменен"}
    return {"message": "Отель не найден"}


@router.patch(
    "/{hotel_id}", 
    summary="Изменить отель частично по ID",
    description="<h1>Изменить отель частично по его ID с его новыми названием и/или городом</h1>",
)
async def partial_update_hotel(hotel_id: int, hotel_data: UpdateHotel):
    for hotel in hotels:
        if hotel["id"] == hotel_id:
            if hotel_data.title:
                hotel["title"] = hotel_data.title
            if hotel_data.name:
                hotel["name"] = hotel_data.name
            return {"message": "Отель успешно изменен"}
    return {"message": "Отель не найден"}