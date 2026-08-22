import asyncio
from decimal import Decimal

from app.core.celery import celery_app
from app.db.celery_session import celery_session_factory
from app.repository.parcels import get_all_parcels_for_task
from app.core.redis import get_redis
from app.service.exchange_rate import get_usd_rate


@celery_app.task
def calculate_delivery_price_task():
    asyncio.run(calculate_delivery_price())


async def calculate_delivery_price():
    async with celery_session_factory() as session:
        parcels = await get_all_parcels_for_task(20, 0, session)
        usd_rate = get_usd_rate(redis_client=get_redis())

        for parcel in parcels:
            delivery_price = (
                parcel.weight * Decimal("0.5") + parcel.dollar_price * Decimal("0.01")
            ) * usd_rate
            parcel.delivery_price = delivery_price

        await session.commit()
