from pydantic import BaseModel, field_validator

from app.exceptions import FacilityTitleDigitHTTPException, FacilityTitleZeroHTTPException


class FacilityAdd(BaseModel):
    title: str

    @field_validator("title")
    @classmethod
    def validate_title(cls, value: str):
        if len(value) <= 1:
            raise FacilityTitleZeroHTTPException
        if any(c.isdigit() for c in value):
            raise FacilityTitleDigitHTTPException
        return value


class Facility(FacilityAdd):
    id: int


class RoomFacilityAdd(BaseModel):
    room_id: int
    facility_id: int


class RoomFacility(RoomFacilityAdd):
    id: int
