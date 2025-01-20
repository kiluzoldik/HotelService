from datetime import date

from fastapi import HTTPException
from pydantic import BaseModel
from sqlalchemy import select
from aiosmtplib import send
from email.message import EmailMessage

from app.models.bookings import Bookings
from app.models.hotels import Hotels
from app.models.rooms import Rooms
from app.repositories.mappers.mappers import BookingDataMapper, RoomDataMapper
from app.repositories.base import BaseRepository
from app.models.users import Users
from app.repositories.utils import get_room_ids_for_booking


class BookingsRepository(BaseRepository):
    model = Bookings
    mapper = BookingDataMapper

    async def send_booking_email(self, user_email: str):
        """Отправить письмо с деталями бронирования."""
        email = EmailMessage()
        email["From"] = "****"
        email["To"] = user_email
        email["Subject"] = "Детали бронирования"
        
        message_body = f"""
        Здравствуйте,

        Ваше бронирование подтверждено.
        """
        email.set_content(message_body)

        # Настройки SMTP-сервера
        smtp_config = {
            "hostname": "smtp.gmail.com",
            "port": 587,
            "start_tls": True,
            "username": "*********",
            "password": "********"
        }
        
        response = await send(email, **smtp_config)
        print(f"Email sent response: {response}")
    
    async def get_user_booking(self, user_id: int):
        user_stmt = (
            select(Users.email)
            .select_from(Users)
            .filter(Users.id == user_id)
        )
        res = await self.session.execute(user_stmt)
        return res.scalars().one()
    
    async def get_bookings_with_today_checkin(self):
        query = (
            select(Bookings)
            .filter(Bookings.date_from == date.today())
        )
        res = await self.session.execute(query)
        lst_bookings = [self.mapper.map_to_domain_entity(booking) for booking in res.scalars().all()]
        for booking in lst_bookings:
            email_user = await self.get_user_booking(booking.user_id)
            print(f"{email_user=}")
            await self.send_booking_email(email_user)
            print("OK")
    
    async def add_booking(self, data: BaseModel):
        stmt = (
            select(Hotels.id)
            .select_from(Hotels)
        )
        result = await self.session.execute(stmt)
        hotel_id = result.scalars().first()
        rooms_ids_for_booking = await get_room_ids_for_booking(data.date_from, data.date_to, hotel_id)
        query = (
            select(Rooms)
            .filter(Rooms.id.in_(rooms_ids_for_booking))
        )
        res = await self.session.execute(query)
        lst = [RoomDataMapper.map_to_domain_entity(object) for object in res.scalars().all()]
        if data.room_id in [obj.id for obj in lst]:
            return await self.add(data)
        else:
            raise HTTPException(status_code=409, detail="Эти номера уже забронированы")
    