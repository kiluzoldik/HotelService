from pydantic import BaseModel, Field


class HotelAdd(BaseModel):
    title: str
    location: str
    
class Hotel(HotelAdd):
    id: int
    
class UpdateHotel(BaseModel):
    title: str | None = Field(None)
    location: str | None = Field(None)
    
class ResponseHotel(BaseModel):
    id: int
    title: str
    location: str