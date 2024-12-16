from pydantic import BaseModel


class FacilityRequest(BaseModel):
    title: str

class Facility(FacilityRequest):
    id: int
