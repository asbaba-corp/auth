from pydantic import BaseModel


class CreateUser(BaseModel):
    email: str
    password: str


class UserResponse(BaseModel):
    email: str
    success: bool
