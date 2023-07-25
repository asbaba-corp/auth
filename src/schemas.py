from pydantic import BaseModel


class CreateUser(BaseModel):
    email: str
    password: str


class UserResponse(BaseModel):
    id: int
    email: str
    success: bool
