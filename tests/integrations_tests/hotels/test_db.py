from app.database import async_session_maker_null_pool
from app.schemas.hotels import HotelAdd
from app.utils.db_manager import DBManager


async def test_add_hotel():
    hotel_data = HotelAdd(title="5STARS", location="Москва")
    async with DBManager(session_factory=async_session_maker_null_pool) as db:
        new_hotel_data = await db.hotels.add(hotel_data)
        await db.commit()
        print(f"{new_hotel_data=}")
        