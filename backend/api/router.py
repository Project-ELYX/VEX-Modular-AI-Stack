from fastapi import APIRouter

from .chat import router as chat_router
from .config import router as config_router

api_router = APIRouter()
api_router.include_router(chat_router, prefix="/chat", tags=["chat"])
api_router.include_router(config_router, prefix="/config", tags=["config"])
