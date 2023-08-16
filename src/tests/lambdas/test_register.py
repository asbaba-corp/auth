from passlib.context import CryptContext
from fastapi.logger import logger as api_logger
from src.db.dynamodb.repositories.users_repository import register
from src.users.schemas import CreateUser
from src.tests.utils import generate_random_string

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def test_register():
    api_logger.info("Start test_register")
    random_str = generate_random_string(3)
    email = f"test{random_str}@example.com"
    hashed_password = pwd_context.hash("password")
    test_user = CreateUser(email=email, password=hashed_password)
    # Call the register function
    register(test_user)

    # user = get_user(email, dynamodb=dynamodb)
    # Check if the user was inserted correctly
    # assert user is not None
    # assert user["email"] == email  # type: ignore # Use `==` for equality comparison
    # api_logger.info("test_register passed successfully")
