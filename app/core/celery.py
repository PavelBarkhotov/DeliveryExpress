from celery import Celery

from app.core.config import settings

celery_app = Celery(
    "delivery_pricer",
    broker=settings.broker_url,
    include=["app.tasks.parcels"],
)

celery_app.conf.enable_utc = True
celery_app.conf.beat_schedule = {
    "calculate-delivery-price-every-5-min": {
        "task": "app.tasks.parcels.calculate_delivery_price_task",
        "schedule": settings.CELERY_TASK_INTERVAL,
    }
}
