from pydantic import BaseModel, Field


class Hotel(BaseModel):
    title: str
    name: str
    
class UpdateHotel(BaseModel):
    title: str | None = Field(None)
    name: str | None = Field(None)