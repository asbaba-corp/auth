import uuid
import json
import hashlib
from datetime import datetime
import boto3
from botocore.exceptions import ClientError


dynamo = boto3.client("dynamodb")

print("Loading lambda function")


def respond(err, res=None):
    return {
        "statusCode": "400" if err else "200",
        "body": err.message if err else json.dumps(res),
        "headers": {
            "Content-Type": "application/json",
        },
    }


def check_existing_user(email):
    try:
        response = dynamo.get_item(
            TableName="Users",
            Key={"email": {"S": email}},
        )
        return "Item" in response
    except ClientError:
        return False


def register_user_in_db(user):
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


def lambda_handler(event, _):  # Context is not being used, so is passed as _
    try:
        payload = json.loads(event["body"])
        email = payload.get("email")
        password = payload.get("password")

        if email and check_existing_user(email):
            return respond(ValueError("Email already exists"))

        # Hash the provided password with the same salt
        salt = "s135"
        db_password = password + salt
        hashed_provided = hashlib.md5(db_password.encode()).hexdigest()

        user = {
            "email": email,
            "password": hashed_provided,
        }
        response = register_user_in_db(user)
        return respond(None, response)
    except Exception as exception:
        return respond(ValueError(str(exception)))
