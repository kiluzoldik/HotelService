from datetime import date

from fastapi import APIRouter, Body, HTTPException, Query
from fastapi_cache.decorator import cache

from app.exceptions import (
    HotelAlreadyExistsException,
    DatefromIsLaterThanDatetoException,
    HotelAlreadyExistsHTTPException,
    HotelNotFoundException,
    HotelNotFoundHTTPException,
    ObjectNotFoundException,
    check_dates,
)
from app.schemas.hotels import HotelAdd, UpdateHotel, Hotel
from app.api.dependencies import PaginationDep
from app.api.dependencies import DBDep
from app.services.hotels import HotelService


router = APIRouter(
    prefix="/hotels",
    tags=["Отели"],
)


@router.get(
    "",
    summary="Получить список всех отелей",
    description="<h1>Получить список всех отелей с их id, названиями и городами</h1>",
    response_model=list[Hotel],
)
@cache(expire=10)
async def get_hotels(
    pagination: PaginationDep,
    db: DBDep,
    title: str | None = Query(None, description="Название отеля"),
    location: str | None = Query(None, description="Город отеля"),
    date_from: date = Query(example="2025-01-12"),
    date_to: date = Query(example="2025-07-27"),
):
    try:
        check_dates(date_from, date_to)
    except DatefromIsLaterThanDatetoException as e:
        raise HTTPException(status_code=422, detail=e.detail)

    return await HotelService(db).get_hotels(
        pagination,
        title,
        location,
        date_from,
        date_to,
    )


@router.get(
    "/{hotel_id}",
    summary="Получить информацию об отеле по ID",
    description="<h1>Получить информацию об отеле по его ID с его названием и городом</h1>",
)
async def get_hotel_by_id(hotel_id: int, db: DBDep):
    try:
        return await HotelService(db).get_hotel_by_id(hotel_id)
    except ObjectNotFoundException:
        raise HotelNotFoundException


@router.post(
    "",
    summary="Создать новый отель",
    description="<h1>Создать новый отель с его названием и городом</h1>",
)
async def create_hotel(
    db: DBDep,
    hotel_data: HotelAdd = Body(
        openapi_examples={
            "1": {
                "summary": "Пример создания нового отеля",
                "value": {"title": "Отель номер 1", "location": "Москва"},
            }
        }
    ),
):
    try:
        hotel = await HotelService(db).create_hotel(hotel_data)
    except HotelAlreadyExistsException:
        raise HotelAlreadyExistsHTTPException
    return {"message": "Отель успешно добавлен", "data": hotel}


@router.delete(
    "/{hotel_id}",
    summary="Удалить отель по ID",
    description="<h1>Удалить отель по его ID</h1>",
)
async def delete_hotel(hotel_id: int, db: DBDep):
    try:
        await HotelService(db).delete_hotel(hotel_id)
    except HotelNotFoundException:
        raise HotelNotFoundHTTPException
    return {"message": "Отель успешно удален"}


@router.put(
    "/{hotel_id}",
    summary="Изменить отель полностью по ID",
    description="<h1>Изменить отель полностью по его ID с его новыми названием и городом</h1>",
)
async def full_update_hotel(hotel_id: int, db: DBDep, hotel_data: UpdateHotel):
    try:
        await HotelService(db).full_update_hotel(hotel_id=hotel_id, hotel_data=hotel_data)
    except HotelNotFoundException:
        raise HotelNotFoundHTTPException
    return {"message": "Отель успешно изменен"}


@router.patch(
    "/{hotel_id}",
    summary="Изменить отель частично по ID",
    description="<h1>Изменить отель частично по его ID с его новыми названием и/или городом</h1>",
)
async def partial_update_hotel(hotel_id: int, db: DBDep, hotel_data: UpdateHotel):
    try:
        await HotelService(db).partial_update_hotel(hotel_id=hotel_id, hotel_data=hotel_data)
    except HotelNotFoundException:
        raise HotelNotFoundHTTPException
    return {"message": "Отель изменен"}
