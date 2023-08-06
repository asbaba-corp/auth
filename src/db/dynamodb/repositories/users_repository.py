import uuid
from datetime import datetime
from botocore.exceptions import ClientError
from src.db.dynamodb.connection import dynamo


def register(user):
    try:
        response = dynamo.put_item(
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


def get_user(email):
    try:
        response = dynamo.get_item(TableName="Users", Key={"email": {"S": email}})
        user = response.get("Item")
        if not user:
            return None
        user_data = {
            "id": user["id"]["S"],
            "email": user["email"]["S"],
            "password": user["password"]["S"],
            "created_at": user["created_at"]["S"],
        }
        return user_data
    except ClientError as exception:
        return {"error": exception.response["Error"]["Message"]}
