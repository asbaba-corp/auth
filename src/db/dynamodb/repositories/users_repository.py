import uuid
from datetime import datetime
from botocore.exceptions import ClientError
from src.db.dynamodb.connection import dynamo


def register(user):
    try:
        response = dynamo.put_item(
            TableName="Users",
            Item={
                "id": str(uuid.uuid4()),
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
