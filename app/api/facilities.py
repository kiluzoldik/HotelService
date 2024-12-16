from fastapi import APIRouter

from app.api.dependencies import DBDep
from app.schemas.facilities import FacilityRequest


router = APIRouter(
    prefix="/facilities",
    tags=["Удобства"]
)

@router.get(
    "",
    summary="Получение всех удобств",
)
async def get_facilities(db: DBDep):
    return await db.facilities.get_all()

@router.post(
    "",
    summary="Добавление удобств для отелей"
)
async def add_facilities(db: DBDep, data: FacilityRequest):
    result = await db.facilities.add(data)
    await db.commit()
    return {"message": "Удобства успешно добавлены", "data": result}