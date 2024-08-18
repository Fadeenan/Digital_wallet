# digimon/main.py

import logging
from fastapi import FastAPI
from contextlib import asynccontextmanager

from . import config, models, routers

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    yield
    if models.engine is not None:
        await models.close_session()

def create_app():
    app = FastAPI(lifespan=lifespan)
    models.init_db(config.get_settings())
    routers.init_router(app)
    
    @app.on_event("startup")
    async def startup_event():
        logger.info("Starting up...")

    @app.on_event("shutdown")
    async def shutdown_event():
        logger.info("Shutting down...")

    return app
