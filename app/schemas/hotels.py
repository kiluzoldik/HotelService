from pydantic import BaseModel, field_validator

from app.exceptions import (
    HotelLocationLengthHTTPException,
    HotelTitileLetterUpperHTTPException,
    HotelTitleLengthHTTPException,
    HotelTitleLetterHTTPException,
)


class HotelAdd(BaseModel):
    title: str
    location: str

    @field_validator("title")
    @classmethod
    def validate_title(cls, value: str):
        if len(value) < 3:
            raise HotelTitleLengthHTTPException
        if not any(simbol.isupper() for simbol in value):
            raise HotelTitileLetterUpperHTTPException
        if not any(simbol.isalpha() for simbol in value):
            raise HotelTitleLetterHTTPException
        return value

    @field_validator("location")
    @classmethod
    def validate_location(cls, value: str):
        if len(value) < 5:
            raise HotelLocationLengthHTTPException
        return value


class Hotel(HotelAdd):
    id: int


class UpdateHotel(BaseModel):
    title: str | None = None
    location: str | None = None
