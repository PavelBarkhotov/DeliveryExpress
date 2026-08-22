import logging
import sys
from pythonjsonlogger.json import JsonFormatter

from app.core.config import settings


def configure_logging() -> None:
    logger = logging.getLogger("app")

    if logger.handlers:
        logger.handlers.clear()

    handler = logging.StreamHandler(sys.stdout)

    if settings.DEBUG:
        # Вывод всех логов в виде строки
        formatter = logging.Formatter(
            "%(asctime)s [%(levelname)s] %(name)s - %(message)s"
        )
        logger.setLevel(logging.DEBUG)

    else:
        # Вывод всех логов в JSON
        formatter = JsonFormatter(
            fmt="%(asctime)s %(levelname)s %(name)s %(message)s",
            rename_fields={"levelname": "level", "asctime": "timestamp"},
        )
        logger.setLevel(logging.INFO)

    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.propagate = False
