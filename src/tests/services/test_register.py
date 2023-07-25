from fastapi.logger import logger as api_logger
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from main import start_application
from src.services import register
from src.models import User
from src.schemas import CreateUser
from src.tests.utils import generate_random_string

TEST_DATABASE_URL = "mysql+pymysql://root:password@localhost:3306/cataprato_database"

engine = create_engine(TEST_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    session = TestingSessionLocal()
    try:
        return session
    finally:
        session.close()


app = start_application()
app.dependency_overrides[get_db] = get_db


def test_register():
    api_logger.info("Start test_register")
    database = get_db()
    random_str = generate_random_string(3)
    email = f"test{random_str}@example.com"
    test_user = CreateUser(email=email, password="password")

    # Call the register function
    user = register(database, test_user, "cognito_username")

    # Check if the user was inserted correctly
    assert user.id is not None
    assert user.email == email  # type: ignore # Use `==` for equality comparison

    # Delete the user from the database
    database.delete(user)
    database.commit()

    # Verify that the user was deleted successfully
    deleted_user = database.query(User).filter(User.email == email).first()
    assert deleted_user is None

    api_logger.info("test_register passed successfully")
