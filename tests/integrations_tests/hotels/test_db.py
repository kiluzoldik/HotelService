from app.schemas.hotels import HotelAdd


async def test_add_hotel(db):
    hotel_data = HotelAdd(title="5STARS", location="Москва")
    await db.hotels.add(hotel_data)
    await db.commit()
        