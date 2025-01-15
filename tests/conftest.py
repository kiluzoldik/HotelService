import pytest

from app.database import Base, engine_null_pool
from app.config import settings
from app.models import *


@pytest.fixture(scope="session", autouse=True)
async def async_main():
    assert settings.MODE == "TEST"
    
    async with engine_null_pool.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)