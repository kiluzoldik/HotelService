from app.models.facilities import Facilities
from app.repositories.base import BaseRepository
from app.schemas.facilities import Facility


class FacilitiesRepository(BaseRepository):
    model = Facilities
    schema = Facility