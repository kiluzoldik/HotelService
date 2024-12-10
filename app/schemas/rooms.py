from pydantic import BaseModel


class AddRoomRequest(BaseModel):
    title: str
    description: str | None = None
    price: int
    quantity: int

class AddRoom(BaseModel):
    hotel_id: int
    title: str
    description: str | None = None
    price: int
    quantity: int
    
class RoomPatchRequest(BaseModel):
    title: str | None = None
    description: str | None = None
    price: int | None = None
    quantity: int | None = None
    
class RoomPatch(BaseModel):
    hotel_id: int | None = None
    title: str | None = None
    description: str | None = None
    price: int | None = None
    quantity: int | None = None
    
class Room(AddRoom):
    id: int