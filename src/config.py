import os
from dotenv import load_dotenv


class AppConfig:
    def __init__(self):
        # Load environment variables from .env file
        load_dotenv()
        self.aws_access_key_id = os.environ.get("AWS_ACCESS_KEY_ID")
        self.aws_secret_access_key = os.environ.get("AWS_SECRET_ACCESS_KEY")
        self.aws_session_token = os.environ.get("AWS_SESSION_TOKEN")
        self.debug_mode = os.environ.get("DEBUG")
        self.database_url = os.environ.get("DATABASE_URL")


config = AppConfig()
