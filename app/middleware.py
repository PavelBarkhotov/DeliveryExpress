from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.requests import Request
from starlette.responses import Response

import logging
import time

logger = logging.getLogger(__name__)


class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(
        self, request: Request, call_next: RequestResponseEndpoint
    ) -> Response:
        start_time = time.perf_counter()
        client_ip = request.client.host if request.client else None
        method = request.method
        url = request.url.path

        logger.info(
            "Получен запрос",
            extra={"client_ip": client_ip, "method": method, "url": url},
        )
        try:
            response = await call_next(request)
            elapsed_time = (time.perf_counter() - start_time) * 1000

            logger.info(
                "Отправлен ответ",
                extra={
                    "client_ip": client_ip,
                    "method": method,
                    "url": url,
                    "status_code": response.status_code,
                    "time_ms": elapsed_time,
                },
            )

            return response
        except Exception:
            elapsed_time = (time.perf_counter() - start_time) * 1000
            logger.exception(
                "Произошла ошибка",
                extra={
                    "client_ip": client_ip,
                    "method": method,
                    "url": url,
                    "time_ms": elapsed_time,
                },
            )
            raise
