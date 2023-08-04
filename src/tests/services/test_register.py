from datetime import datetime
from fastapi.logger import logger as api_logger
from main import start_application
from src.db.dynamodb.repositories.users_repository import register
from src.users.schemas import CreateUser
from src.tests.utils import generate_random_string

app = start_application()


def test_register():
    api_logger.info("Start test_register")
    random_str = generate_random_string(3)
    email = f"test{random_str}@example.com"
    test_user = CreateUser(email=email, password="password")
    user = {
        "email": test_user.email,
        "password": test_user.password,
        "created_at": datetime.utcnow().isoformat(),
    }
    # Call the register function
    register(user)

    # user = get_user(email, dynamodb=dynamodb)
    # Check if the user was inserted correctly
    # assert user is not None
    # assert user["email"] == email  # type: ignore # Use `==` for equality comparison
    # api_logger.info("test_register passed successfully")
