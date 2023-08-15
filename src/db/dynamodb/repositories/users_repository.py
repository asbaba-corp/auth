import uuid
from datetime import datetime
from botocore.exceptions import ClientError
from users.exceptions import UserNotFoundException
from exceptions import DatabaseError
from db.dynamodb.connection import dynamo as dynamodb


def register(user):
    try:
        user_id = str(uuid.uuid4())
        created_at = datetime.utcnow().isoformat()
        query = (
            f"INSERT INTO Users (id, email, password, created_at) "
            f"VALUES ('{user_id}', '{user['email']}', '{user['password']}', '{created_at}')"
        )
        response = dynamodb.execute_statement(Statement=query)
        return response
    except ClientError as exception:
        raise DatabaseError(
            f"Database error: {exception.response['Error']['Message']}"
        ) from exception


def get_user(email):
    try:
        query = f"SELECT * FROM Users WHERE email = '{email}'"
        response = dynamodb.execute_statement(
            Statement=query,
        )
        user = response["Items"][0]
        if not user:
            raise UserNotFoundException(f"User with email '{email}' not found")
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
