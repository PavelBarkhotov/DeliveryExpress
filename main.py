from fastapi import FastAPI

app = FastAPI()

app.title = "Delivery Express"

@app.get("/health")
def health():
    return {"status": "ok"}