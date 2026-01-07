from fastapi import FastAPI
from .routers import router as requests_router

app = FastAPI(title="BINDO API")

app.include_router(requests_router, prefix="/api/v1/requests")

@app.get("/health")
def health():
    return {"status": "ok"}
