from fastapi import FastAPI

from app.api.v1.parcels import router as parcels_router
from app.core.logging import configure_logging
from app.middleware import LoggingMiddleware

configure_logging()

app = FastAPI()

app.title = "Delivery Express"

app.add_middleware(LoggingMiddleware)

@app.get("/health")
def health():
    return {"status": "ok"}

app.include_router(parcels_router, prefix="/api/v1", tags=["Посылки"])