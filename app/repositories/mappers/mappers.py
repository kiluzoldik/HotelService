from app.models.bookings import Bookings
from app.models.facilities import Facilities
from app.models.hotels import Hotels
from app.models.rooms import Rooms
from app.models.users import Users
from app.repositories.mappers.base import DataMapper
from app.schemas.bookings import Booking
from app.schemas.facilities import Facility
from app.schemas.hotels import Hotel
from app.schemas.rooms import Room, RoomWithRelationship
from app.schemas.users import User, UserWithHashedPassword


class HotelDataMapper(DataMapper):
    db_model = Hotels
    schema = Hotel


class UserDataMapper(DataMapper):
    db_model = Users
    schema = User


class RoomDataMapper(DataMapper):
    db_model = Rooms
    schema = Room


class BookingDataMapper(DataMapper):
    db_model = Bookings
    schema = Booking


class FacilityDataMapper(DataMapper):
    db_model = Facilities
    schema = Facility


class RoomWithRelationshipDataMapper(DataMapper):
    db_model = Rooms
    schema = RoomWithRelationship


class UserWithHashedPasswordDataMapper(DataMapper):
    db_model = Users
    schema = UserWithHashedPassword
