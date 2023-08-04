from pydantic import BaseModel
import bcrypt


class CreateUser(BaseModel):
    email: str
    password: str

    def hash_password(self, password: str) -> str:
        # Generate a salt and hash the password
        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(password.encode("utf-8"), salt)
        return hashed_password.decode("utf-8")


class UserResponse(BaseModel):
    email: str
    success: bool
