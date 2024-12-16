from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import ForeignKey, String

from app.database import Base


class Facilities(Base):
    __tablename__ = "facilities"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    title:Mapped[str] = mapped_column(String(100))
    
    
class RoomsFacilities(Base):
    __tablename__ = "rooms_facilities"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    room_id: Mapped[int] = mapped_column(ForeignKey("rooms.id"))
    facility_id: Mapped[int] = mapped_column(ForeignKey("facilities.id"))