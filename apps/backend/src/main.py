from fastapi import FastAPI
from src.api import api_router
from src.core.config import settings

app = FastAPI(
    title=settings.PROJECT_NAME,
    description="API for managing tournament scores and brackets",
    version=settings.VERSION,
)

app.include_router(api_router, prefix=settings.API_V1_STR)


@app.get("/")
async def root():
    return {"message": f"Welcome to {settings.PROJECT_NAME} API"}
