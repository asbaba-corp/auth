import boto3
from config import config

session = boto3.session.Session(  # type: ignore
    aws_access_key_id=config.aws_access_key_id,
    aws_secret_access_key=config.aws_secret_access_key,
    aws_session_token=config.aws_session_token,
)
dynamo = session.client("dynamodb", region_name="us-east-1")
