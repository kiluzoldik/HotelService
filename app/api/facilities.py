from fastapi import APIRouter, Body

from app.api.dependencies import DBDep
from app.schemas.facilities import FacilityAdd


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
async def add_facilities(db: DBDep, data: FacilityAdd = Body()):
    result = await db.facilities.add(data)
    await db.commit()
    return {"message": "Удобства успешно добавлены", "data": result}