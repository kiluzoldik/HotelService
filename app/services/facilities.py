from app.schemas.facilities import FacilityAdd
from app.services.base import BaseService
from app.tasks.tasks import test_task


class FacilityService(BaseService):
    async def add_facilities(self, data: FacilityAdd):
        result = await self.db.facilities.add(data)
        await self.db.commit()

        test_task.delay()
        return result
