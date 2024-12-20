from contextlib import asynccontextmanager

from fastapi import FastAPI
import uvicorn
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend

import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))

from app.api.hotels import router as router_hotels
from app.api.auth import router as auth_router
from app.api.rooms import router as router_rooms
from app.api.bookings import router as router_bookings
from app.api.facilities import router as router_facilities
from app.api.images import router as router_images
from app.setup_redis import redis_connector


@asynccontextmanager
async def lifespan(_: FastAPI):
    await redis_connector.connect()
    FastAPICache.init(RedisBackend(redis_connector), prefix="fastapi-cache")
    yield
    await redis_connector.close()


app = FastAPI(lifespan=lifespan)


app.include_router(auth_router)
app.include_router(router_hotels)
app.include_router(router_rooms)
app.include_router(router_bookings)
app.include_router(router_facilities)
app.include_router(router_images)


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)