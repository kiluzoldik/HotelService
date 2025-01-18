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
        
@pytest.fixture(scope="session")
async def ac() -> AsyncClient:
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        yield ac
        
@pytest.fixture(scope="session", autouse=True)
async def register_user(setup_database, ac):
    await ac.post(
        "/auth/register",
        json={
            "email": "test@test.com",
            "password": "test"
        }
    )
        
@pytest.fixture(scope="function")
async def db() -> DBManager:
    async with DBManager(session_factory=async_session_maker_null_pool) as db:
        yield db
        
@pytest.fixture(scope="session", autouse=True)
async def add_data_to_db(register_user):
    with open("tests/mock_hotels.json", "r") as file:
        hotels_json_data = json.load(file)
    with open("tests/mock_rooms.json", "r") as file:
        rooms_json_data = json.load(file) 
   
    list_hotels_models = [HotelAdd.model_validate(data) for data in hotels_json_data]
    list_rooms_models = [AddRoom.model_validate(data) for data in rooms_json_data]
    async with DBManager(session_factory=async_session_maker_null_pool) as db_:
        await db_.hotels.add_bulk(list_hotels_models)
        await db_.rooms.add_bulk(list_rooms_models)
        await db_.commit()
        