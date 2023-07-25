from fastapi.logger import logger as api_logger
from sqlalchemy.orm import Session
from src.schemas import CreateUser
from src.models import User


def register(database: Session, user: CreateUser, cognito_username: str):
    api_logger.info("Start register service")
    try:
        db_user = User(
            email=user.email, password=user.password, cognito_username=cognito_username
        )
        database.add(db_user)
        database.commit()
        database.refresh(db_user)
        api_logger.info("User created")
        return db_user
    except Exception as exception:
        api_logger.error("Error creating the user in the db: %s", exception)
        raise exception
