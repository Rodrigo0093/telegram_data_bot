# bot/handlers/__init__.py
from aiogram import Dispatcher
from .base import router as base_router
from .filters import router as filters_router

def register_handlers(dp: Dispatcher):
    dp.include_router(base_router)
    dp.include_router(filters_router)
