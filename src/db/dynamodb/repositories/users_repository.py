import uuid
from datetime import datetime

from botocore.exceptions import ClientError

from db.dynamodb.connection import dynamo as dynamodb
from exceptions import DatabaseError
from users.exceptions import UserNotFoundException


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
        raise DatabaseError(
            f"Database error: {exception.response['Error']['Message']}"
        ) from exception


def get_user(email):
    try:
        response = dynamodb.get_item(TableName="Users", Key={"email": {"S": email}})
        user = response.get("Item")
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


def get_all_users():
    try:
        response = dynamodb.scan(TableName="Users")
        users_list = [
            {"id": user["id"], "email": user["email"], "created_at": user["created_at"]}
            for user in response["Items"]
        ]
        return users_list
    except ClientError as exception:
        raise DatabaseError(
            f"Database error: {exception.response['Error']['Message']}"
        ) from exception
