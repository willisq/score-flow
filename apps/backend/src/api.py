from fastapi import APIRouter
from src.features.registration.api.routes import router as registration_router
from src.features.tournament.api.routes import router as tournament_router

api_router = APIRouter()

api_router.include_router(registration_router)
api_router.include_router(tournament_router)
