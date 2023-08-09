from datetime import timedelta, datetime
from fastapi import APIRouter, HTTPException, status
from jose import jwt
from passlib.context import CryptContext
from  db.dynamodb.repositories.users_repository import get_user, register
from  users.config import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES
from  users.schemas import CreateUser
from  users.exceptions import UserNotFoundException

from  exceptions import handle_response  # type: ignore


router = APIRouter()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def create_access_token(data: dict, expires_delta: timedelta):
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


@router.post("/register")
def register_user(request: CreateUser):
    try:
        user = get_user(request.email)
        return user
    except UserNotFoundException:
        hashed_password = pwd_context.hash(request.password)

        user = {
            "email": request.email,
            "password": hashed_password,
        }
        register(user)

        expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token({"sub": request.email}, expires)

        return {"message": "User registered successfully", "access_token": access_token}


@router.post("/auth")
def login(request: CreateUser):
    try:
        user = get_user(request.email)
        if not pwd_context.verify(request.password, user["password"]):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect password",
            )

        expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token({"sub": request.email}, expires)

        return {"message": "Login successful", "access_token": access_token}
    except UserNotFoundException:
        return handle_response(str(UserNotFoundException), 404)
