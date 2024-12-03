from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase

from app.config import settings


engine = create_async_engine(settings.DB_URL)
session_maker = async_sessionmaker(bind=engine)


class Base(DeclarativeBase):
    pass