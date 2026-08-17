from fastapi import FastAPI

from app.api.v1.parcels import router as parcels_router
app = FastAPI()

app.title = "Delivery Express"

@app.get("/health")
def health():
    return {"status": "ok"}

app.include_router(parcels_router, prefix="/api/v1", tags=["Посылки"])