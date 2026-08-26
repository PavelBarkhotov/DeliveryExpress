import asyncio
import logging
from decimal import Decimal

from app.core.celery import celery_app
from app.core.redis import get_redis
from app.db.celery_session import celery_session_factory
from app.repository.parcels import get_all_parcels_for_task
from app.service.exchange_rate import get_usd_rate

logger = logging.getLogger(__name__)


@celery_app.task
def calculate_delivery_price_task():
    asyncio.run(calculate_delivery_price())


async def calculate_delivery_price():
    async with celery_session_factory() as session:
        logger.info("Начато выполнение задачи расчета стоимости посылок")
        usd_rate = get_usd_rate(redis_client=get_redis())
        calc_parcels_count = 0
        while True:
            parcels = await get_all_parcels_for_task(20, session)

            if not parcels:
                logger.info(
                    "Задача завершила расчет стоимости посылок",
                    extra={"calculated_parcels_count": calc_parcels_count},
                )
                break

            for parcel in parcels:
                delivery_price = (
                    parcel.weight * Decimal("0.5")
                    + parcel.dollar_price * Decimal("0.01")
                ) * usd_rate
                parcel.delivery_price = delivery_price

            await session.commit()

            calc_parcels_count += len(parcels)

            logger.info(
                "Расчет стоимости доставки для пачки посылок завершен",
                extra={"parcels_count": len(parcels)},
            )
