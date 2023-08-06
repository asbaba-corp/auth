import uuid
import logging
from datetime import datetime, timedelta
import os
from jose import jwt
from botocore.exceptions import ClientError
from passlib.context import CryptContext

from fastapi import FastAPI, HTTPException, status
from fastapi.logger import logger as api_logger
from fastapi.middleware.cors import CORSMiddleware
from mangum import Mangum
from src.db.dynamodb.connection import dynamo as dynamodb
from src.db.dynamodb.repositories.users_repository import get_user
from src.users.routes import route

from src.users.schemas import CreateUser

STAGE = os.environ.get("STAGE")
root_path = "/" if not STAGE else f"/{STAGE}"
app = FastAPI(title="cataprato_auth", version="v1", root_path=root_path)

logger = logging.getLogger("uvicorn.access")
logger_handler = logging.StreamHandler()
logger_handler.setFormatter(
    logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
)
logger.addHandler(logger_handler)
api_logger.setLevel(logging.DEBUG)
api_logger.info("Starting application")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(route)
# Mangum Handler, this is so important
handler = Mangum(app)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

SECRET_KEY = "your-secret-key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


def create_access_token(data: dict, expires_delta: timedelta):
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def register(user):
    try:
        response = dynamodb.put_item(
            TableName="Users",
            Item={
                "id": {"S": str(uuid.uuid4())},
                "email": {"S": user["email"]},
                "password": {"S": user["password"]},
                "created_at": {
                    "S": datetime.utcnow().isoformat(),
                },
            },
        )
        return response
    except ClientError as exception:
        return {"error": exception.response["Error"]["Message"]}


@app.post("/register")
def register_user(request: CreateUser):
    try:
        user = get_user(request.email)

        if user:
            return {"message": "User already exists"}

        # Hash the password
        hashed_password = pwd_context.hash(request.password)

        user = {
            "email": request.email,
            "password": hashed_password,
        }
        register(user)

        # Generate JWT token
        expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token({"sub": request.email}, expires)

        return {"message": "User registered successfully", "access_token": access_token}
    except Exception as generic_exception:
        # Handle specific errors if needed
        error_message = str(generic_exception)
        raise HTTPException(
            status_code=500, detail=f"Internal server error: {error_message}"
        ) from generic_exception


@app.post("/auth")
def login(request: CreateUser):
    user = get_user(request.email)
    if not user:
        return {"message": "User doesn't exist"}

    # Verify password
    if not pwd_context.verify(request.password, user["password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect password",
        )

    # Generate JWT token
    expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token({"sub": request.email}, expires)

    return {"message": "Login successful", "access_token": access_token}
