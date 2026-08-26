from redis import Redis

from app.core.config import settings


def get_redis() -> Redis:
    return Redis(
        host=settings.REDIS_HOST,
        port=settings.REDIS_PORT,
        db=settings.REDIS_CACHE_DB,
        decode_responses=True,
    )
