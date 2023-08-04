import logging

from fastapi import FastAPI
from fastapi.logger import logger as api_logger
from fastapi.middleware.cors import CORSMiddleware
from src.users.routes import route


def start_application():
    logger = logging.getLogger("uvicorn.access")
    handler = logging.StreamHandler()
    handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))
    logger.addHandler(handler)
    api_logger.setLevel(logging.DEBUG)
    api_logger.info("Starting application")
    app = FastAPI(title="cataprato_auth", version="v1")
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(route)

    return app


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(start_application, host="0.0.0.0", port=8000)
