from typing import Annotated

from fastapi import APIRouter, Body, Form, Query
from sqlalchemy import insert, select, func

from app.models.hotels import Hotels
from app.schemas.hotels import Hotel, UpdateHotel, ResponseHotel
from app.api.dependencies import PaginationDep
from app.database import async_session_maker
from app.repositories.hotels import HotelsRepository
from app.repositories.base import BaseRepository


router = APIRouter(
    prefix="/hotels",
    tags=["Отели"],
)


@router.get(
    "", 
    summary="Получить список всех отелей",
    description="<h1>Получить список всех отелей с их id, названиями и городами</h1>",
    response_model=list[ResponseHotel],
)
async def get_hotels(
    pagination: PaginationDep,
    title: str | None = Query(None, description="Название отеля"),
    location: str | None = Query(None, description="Город отеля"),
):
    per_page = pagination.per_page
    async with async_session_maker() as session:
        return await HotelsRepository(session).get_all(
            title=title,
            location=location,
            limit=per_page,
            offset=(pagination.page - 1) * per_page,
        )


@router.post(
    "", 
    summary="Создать новый отель",
    description="<h1>Создать новый отель с его названием и городом</h1>",
)
async def create_hotel(hotel_data: Hotel = Body(openapi_examples={
    "1": {
        "summary": "Пример создания нового отеля",
        "value": {
            "title": "Отель номер 1",
            "location": "Москва"
        }
    }    
})
):
    async with async_session_maker() as session:
        hotel = await HotelsRepository(session).add(hotel_data)
        await session.commit()
        
    return {"message": "Отель успешно добавлен", "data": hotel}


@router.delete(
    "/{hotel_id}", 
    summary="Удалить отель по ID",
    description="<h1>Удалить отель по его ID</h1>",
)
async def delete_hotel(hotel_id: int):
    async with async_session_maker() as session:
        await HotelsRepository(session).delete(
            hotel_id,
            message="Отель не найден"
        )
        
    return {"message": "Отель успешно удален"}


@router.put(
    "/{hotel_id}", 
    summary="Изменить отель полностью по ID",
    description="<h1>Изменить отель полностью по его ID с его новыми названием и городом</h1>",
)
async def full_update_hotel(hotel_id: int, hotel_data: UpdateHotel):
    async with async_session_maker() as session:
        hotel = await HotelsRepository(session).edit(
            hotel_id,
            hotel_data,
            message="Отель не найден",
        )
        await session.commit()
        await session.refresh(hotel)
    
    return {"message": "Отель успешно изменен"}


# @router.patch(
#     "/{hotel_id}", 
#     summary="Изменить отель частично по ID",
#     description="<h1>Изменить отель частично по его ID с его новыми названием и/или городом</h1>",
# )
# async def partial_update_hotel(hotel_id: int, hotel_data: UpdateHotel):
#     for hotel in hotels:
#         if hotel["id"] == hotel_id:
#             if hotel_data.title:
#                 hotel["title"] = hotel_data.title
#             if hotel_data.name:
#                 hotel["name"] = hotel_data.name
#             return {"message": "Отель успешно изменен"}
#     return {"message": "Отель не найден"}