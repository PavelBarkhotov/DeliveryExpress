import json
import logging
from decimal import Decimal
from typing import Any

import httpx
import redis
from httpx import HTTPStatusError, RequestError
from redis import Redis

from app.core.config import settings

logger = logging.getLogger(__name__)


def parse_rate(value: Any) -> Decimal:
    return Decimal(str(value))


def get_usd_rate(redis_client: Redis) -> Decimal:
    cached_usd_rate = None

    try:
        cached_usd_rate = redis_client.get("usd")
    except redis.exceptions.ConnectionError:
        logger.warning("Редис не доступен")

    if cached_usd_rate is not None:
        logger.debug("Курс доллара взят из redis")
        return parse_rate(cached_usd_rate)

    try:
        result = httpx.get(settings.CBR_URL, timeout=5)
        result.raise_for_status()
        logger.debug("Курс доллара взят с помощью API ЦБ")
    except HTTPStatusError:
        logger.error("API ЦБ недоступен")
        raise
    except RequestError:
        logger.error("Ошибка при запросе")
        raise

    try:
        data = result.json()
    except json.JSONDecodeError:
        raise ValueError("Ошибка получения курса")

    try:
        usd_rate = parse_rate(data["Valute"]["USD"]["Value"])
    except (KeyError, TypeError):
        raise KeyError("Значение курса доллара не найдено")

    try:
        redis_client.set("usd", str(usd_rate), ex=settings.USD_RATE_TTL)
    except redis.exceptions.ConnectionError:
        logger.warning("Редис не доступен")

    return usd_rate
