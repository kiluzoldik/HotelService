from app.connectors.redis_connector import RedisConnector
from app.config import settings


redis_connector = RedisConnector(
    host=settings.REDIS_HOST,
    port=settings.REDIS_PORT,
)
