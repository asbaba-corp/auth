import json
import hashlib
from fastapi import APIRouter, HTTPException

from src.users.schemas import CreateUser
from src.users.aws_lambdas.register_user import lambda_handler
from src.db.dynamodb.repositories.users_repository import register

route = APIRouter()


@route.post("/lambda/register")
def lambda_register_user(request: CreateUser):
    try:
        # Hash the provided password with the same salt
        salt = "s135"
        db_password = request.password + salt
        hashed_provided = hashlib.md5(db_password.encode()).hexdigest()

        # Assuming `request.email` and `hashed_provided` are defined somewhere
        user = {
            "email": request.email,
            "password": hashed_provided,
        }

        event = {
            "body": json.dumps(user)  # Convert the user dictionary to a JSON string
        }

        # Call Lambda handler function with the constructed event
        result = lambda_handler(event, None)

        return result
    except Exception as generic_exception:
        # Handle specific errors if needed
        error_message = str(generic_exception)
        raise HTTPException(
            status_code=500, detail=f"Internal server error: {error_message}"
        ) from generic_exception


@route.post("/register")
def register_user(request: CreateUser):
    try:
        # Hash the provided password with the same salt
        salt = "s135"
        db_password = request.password + salt
        hashed_provided = hashlib.md5(db_password.encode()).hexdigest()

        user = {
            "email": request.email,
            "password": hashed_provided,
        }
        result = register(user)
        return result
    except Exception as generic_exception:
        # Handle specific errors if needed
        error_message = str(generic_exception)
        raise HTTPException(
            status_code=500, detail=f"Internal server error: {error_message}"
        ) from generic_exception
