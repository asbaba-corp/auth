import json
import hashlib
from fastapi.logger import logger as api_logger
from  tests.utils import generate_random_string
from  users.aws_lambdas.register_user import lambda_handler


def test_register():
    api_logger.info("Start test_register")

    random_str = generate_random_string(3)
    email = f"test{random_str}@example.com"
    salt = "s135"
    db_password = "password" + salt
    hashed_provided = hashlib.md5(db_password.encode()).hexdigest()

    user = {
        "email": email,
        "password": hashed_provided,
    }

    event = {"body": json.dumps(user)}  # Convert the user dictionary to a JSON string

    # Call the register function
    lambda_handler(event, None)

    # user = get_user(email, dynamodb=dynamodb)
    # Check if the user was inserted correctly
    assert user is not None
    assert user["email"] == email  # type: ignore # Use `==` for equality comparison
    api_logger.info("test_register passed successfully")
