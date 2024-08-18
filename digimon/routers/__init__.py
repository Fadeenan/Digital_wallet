# digimon/routers/__init__.py

from fastapi import APIRouter
from .items import router as items_router
from .merchants import router as merchants_router
from .users import router as users_router
from .authentication import router as auth_router
from .wallets import router as wallets_router
from .transactions import router as transactions_router

def init_router(app):
    app.include_router(items_router)
    app.include_router(merchants_router)
    app.include_router(users_router)
    app.include_router(auth_router)
    app.include_router(wallets_router)
    app.include_router(transactions_router)
