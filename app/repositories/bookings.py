from app.models.bookings import Bookings
from app.schemas.bookings import Booking
from repositories.base import BaseRepository


class BookingsRepository(BaseRepository):
    model = Bookings
    schema = Booking
