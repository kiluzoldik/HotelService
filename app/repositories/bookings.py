from datetime import date

from sqlalchemy import select
from aiosmtplib import send
from email.message import EmailMessage

from app.models.bookings import Bookings
from app.repositories.mappers.mappers import BookingDataMapper
from app.repositories.base import BaseRepository
from app.models.users import Users


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
    