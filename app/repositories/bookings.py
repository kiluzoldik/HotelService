from app.models.bookings import Bookings
from app.repositories.mappers.mappers import BookingDataMapper
from repositories.base import BaseRepository


class BookingsRepository(BaseRepository):
    model = Bookings
    mapper = BookingDataMapper
