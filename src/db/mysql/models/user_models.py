from sqlalchemy import Column, Integer, String
from src.db.mysql.connection import Base


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True)
    password = Column(String)
    cognito_username = Column(String)


RAW_QUERY = """CREATE TABLE users (
            id INT AUTO_INCREMENT PRIMARY KEY,
            email VARCHAR(255) UNIQUE NOT NULL,
            password VARCHAR(255) NOT NULL,
            cognito_username VARCHAR(255)
        )"""
