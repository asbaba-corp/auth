import uuid
from src.db.dynamodb.connection import dynamo as dynamodb

TABLE_NAME = "Users"

response = dynamodb.scan(TableName=TABLE_NAME)
items = response["Items"]


def run_migration():
    print("Running migration")
    for item in items:
        email = item["email"]["S"]
        user_id = str(uuid.uuid4())
        created_at = item["created_at"]["S"]

        update_expression = "SET #id = :id_val, created_at = :created_at_val"
        expression_attribute_names = {"#id": "id"}
        expression_attribute_values = {
            ":id_val": {"S": user_id},
            ":created_at_val": {"S": created_at},
        }

        dynamodb.update_item(
            TableName=TABLE_NAME,
            Key={"email": {"S": email}},
            UpdateExpression=update_expression,
            ExpressionAttributeNames=expression_attribute_names,
            ExpressionAttributeValues=expression_attribute_values,
        )
