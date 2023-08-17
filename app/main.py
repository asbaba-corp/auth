from fastapi import FastAPI
from fastapi.logger import logger as api_logger
from mangum import Mangum
from .users.routes import router as user_router

app = FastAPI(title="cataprato_auth", version="v1")

api_logger.info("Starting application")

app.include_router(user_router)

handler = Mangum(app)
