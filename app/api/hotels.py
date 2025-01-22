from datetime import date

from fastapi import APIRouter, Body, HTTPException, Query
from fastapi_cache.decorator import cache

from app.exceptions import DatefromIsLaterThanDatetoException, ObjectNotFoundException
from app.schemas.hotels import HotelAdd, UpdateHotel, Hotel
from app.api.dependencies import PaginationDep
from app.api.dependencies import DBDep


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
    per_page = pagination.per_page
    try:
        result = await db.hotels.get_hotels_by_date(
            title=title,
            location=location,
            date_from=date_from,
            date_to=date_to,
            limit=per_page,
            offset=(pagination.page - 1) * per_page,
        )
    except DatefromIsLaterThanDatetoException as e:
        raise HTTPException(status_code=422, detail=e.detail)
    
    return result


@router.get(
    "/{hotel_id}",
    summary="Получить информацию об отеле по ID",
    description="<h1>Получить информацию об отеле по его ID с его названием и городом</h1>",
)
async def get_hotel_by_id(hotel_id: int, db: DBDep):
    try:
        result = await db.hotels.get_one(id=hotel_id)
    except ObjectNotFoundException:
        raise HTTPException(status_code=404, detail="Отель не найден")
    
    return result


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
    hotel = await db.hotels.add(hotel_data)
    await db.commit()

    return {"message": "Отель успешно добавлен", "data": hotel}


@router.delete(
    "/{hotel_id}",
    summary="Удалить отель по ID",
    description="<h1>Удалить отель по его ID</h1>",
)
async def delete_hotel(hotel_id: int, db: DBDep):
    await db.hotels.delete(id=hotel_id)
    await db.commit()

    return {"message": "Отель успешно удален"}


@router.put(
    "/{hotel_id}",
    summary="Изменить отель полностью по ID",
    description="<h1>Изменить отель полностью по его ID с его новыми названием и городом</h1>",
)
async def full_update_hotel(hotel_id: int, db: DBDep, hotel_data: UpdateHotel):
    await db.hotels.edit(hotel_data, id=hotel_id)
    await db.commit()

    return {"message": "Отель успешно изменен"}


@router.patch(
    "/{hotel_id}",
    summary="Изменить отель частично по ID",
    description="<h1>Изменить отель частично по его ID с его новыми названием и/или городом</h1>",
)
async def partial_update_hotel(hotel_id: int, db: DBDep, hotel_data: UpdateHotel):
    await db.hotels.edit(hotel_data, exclude_unset=True, id=hotel_id)
    await db.commit()

    return {"message": "Отель изменен"}
