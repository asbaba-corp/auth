import uuid
from datetime import datetime
from botocore.exceptions import ClientError
from src.users.schemas import CreateUser
from src.users.exceptions import UserNotFoundException
from src.exceptions import DatabaseError
from src.db.dynamodb.connection import dynamo as dynamodb


def register(user: CreateUser):
    try:
        user_id = str(uuid.uuid4())
        created_at = datetime.utcnow().isoformat()
        value = {
            "id": user_id,
            "email": user.email,
            "password": user.password,
            "created_at": created_at,
        }
        query = f"""
        INSERT INTO Users
        VALUE {value}
        """
        response = dynamodb.execute_statement(Statement=query)
        return response
    except ClientError as exception:
        raise DatabaseError(
            f"Database error: {exception.response['Error']['Message']}"
        ) from exception


def get_user(email: str):
    try:
        query = f"SELECT * FROM Users WHERE email = '{email}'"
        response = dynamodb.execute_statement(
            Statement=query,
        )

        if not response["Items"]:
            raise UserNotFoundException(f"User with email '{email}' not found")
        user = response["Items"][0]
        user_data = {
            "id": user["id"]["S"],
            "email": user["email"]["S"],
            "password": user["password"]["S"],
            "created_at": user["created_at"]["S"],
        }
        return user_data
    except ClientError as exception:
        raise DatabaseError(
            f"Database error: {exception.response['Error']['Message']}"
        ) from exception
