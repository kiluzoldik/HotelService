from fastapi import APIRouter, Body
from fastapi_cache.decorator import cache

from app.api.dependencies import DBDep
from app.schemas.facilities import FacilityAdd
from app.services.facilities import FacilityService


router = APIRouter(prefix="/facilities", tags=["Удобства"])


@router.get(
    "",
    summary="Получение всех удобств",
)
@cache(expire=10)
async def get_facilities(db: DBDep):
    return await db.facilities.get_all()


@router.post("", summary="Добавление удобств для отелей")
async def add_facilities(db: DBDep, data: FacilityAdd = Body()):
    result = await FacilityService(db).add_facilities(data)
    return {"message": "Удобства успешно добавлены", "data": result}
