import json
import pytest
from httpx import ASGITransport, AsyncClient

from app.database import Base, engine_null_pool
from app.config import settings
from app.models import *
from app.main import app
from app.database import async_session_maker_null_pool
from app.schemas.rooms import AddRoom
from app.utils.db_manager import DBManager
from app.schemas.hotels import HotelAdd


@pytest.fixture(scope="session", autouse=True)
async def check_mode():
    assert settings.MODE == "TEST"

@pytest.fixture(scope="session", autouse=True)
async def setup_database(check_mode):
    
    async with engine_null_pool.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
        
@pytest.fixture(scope="session", autouse=True)
async def register_user(setup_database):
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        await ac.post(
            "/auth/register",
            json={
                "email": "test@test.com",
                "password": "test"
            }
        )
        
@pytest.fixture(scope="session", autouse=True)
async def add_data_to_db(register_user):
    with open("tests/mock_hotels.json", "r") as file:
        hotels_json_data = json.loads(file.read())
        list_hotels_models = []
        for data in hotels_json_data:
            new_data = HotelAdd.model_validate(data)
            list_hotels_models.append(new_data)
        async with DBManager(session_factory=async_session_maker_null_pool) as db:
            await db.hotels.add_bulk(list_hotels_models)
            await db.commit()
        
    with open("tests/mock_rooms.json", "r") as file:
        rooms_json_data = json.loads(file.read())
        list_rooms_models = []
        for data in rooms_json_data:
            new_data = AddRoom.model_validate(data)
            list_rooms_models.append(new_data)
        async with DBManager(session_factory=async_session_maker_null_pool) as db:
            await db.rooms.add_bulk(list_rooms_models)
            await db.commit()
        