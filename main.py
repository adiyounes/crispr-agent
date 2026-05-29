from fastapi import FastAPI
from api.router import router
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI(
    title="CRISPR  Analysis API",
    description="API for analyzing CRISPR off-target effects based on gene variants.",)
app.include_router(router, prefix="/api/v1/crispr")


app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
async def health_check():
    return {"status": "ok"}