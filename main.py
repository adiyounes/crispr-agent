from fastapi import FastAPI
from api.router import router

app = FastAPI(
    title="CRISPR  Analysis API",
    description="API for analyzing CRISPR off-target effects based on gene variants.",)
app.include_router(router, prefix="/api/v1/crispr")


@app.get("/health")
async def health_check():
    return {"status": "ok"}