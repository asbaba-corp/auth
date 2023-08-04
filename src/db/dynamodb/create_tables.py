import boto3


def create_users_table(dynamodb=None):
    if not dynamodb:
        dynamodb = boto3.resource("dynamodb", endpoint_url="http://localhost:8000")

    table = dynamodb.create_table(  # type: ignore
        TableName="Users",
        KeySchema=[
            {"AttributeName": "name", "KeyType": "HASH"},  # Partition key
            {"AttributeName": "occupation", "KeyType": "RANGE"},  # Sort key
        ],
        AttributeDefinitions=[
            {"AttributeName": "name", "AttributeType": "S"},
            {"AttributeName": "occupation", "AttributeType": "S"},
        ],
        ProvisionedThroughput={"ReadCapacityUnits": 1, "WriteCapacityUnits": 1},
    )
    return table
