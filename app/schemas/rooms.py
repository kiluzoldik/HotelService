from pydantic import BaseModel, Field


class AddRoom(BaseModel):
    hotel_id: int
    title: str
    description: str | None
    price: int
    quantity: int
    
class UpdateRoom(BaseModel):
    title: str | None = Field(None)
    description: str | None = Field(None)
    price: int | None = Field(None)
    quantity: int | None = Field(None)
    
class Room(AddRoom):
    id: int