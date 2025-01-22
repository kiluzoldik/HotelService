from datetime import date

from pydantic import BaseModel


class AddBookingRequest(BaseModel):
    room_id: int
    date_from: date
    date_to: date


class AddBooking(BaseModel):
    room_id: int
    user_id: int
    date_from: date
    date_to: date
    price: int


class Booking(AddBooking):
    id: int
