from datetime import timedelta, datetime
from fastapi import APIRouter, HTTPException, status
from jose import jwt, JWTError
from passlib.context import CryptContext
from app.db.dynamodb.repositories.users_repository import get_user, register
from app.users.config import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES
from app.users.schemas import CreateUser, UserResponse
from app.users.exceptions import (
    UserAlreadyExistsException,
    UserNotFoundException,
    InvalidCredentialsException,
)

from app.exceptions import handle_response  # type: ignore


router = APIRouter()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def create_access_token(data: dict, expires_delta: timedelta):
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def get_current_user(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")  # type: ignore
        if email is None:
            return handle_response(str(UserNotFoundException), 404)
        return email
    except JWTError:
        return handle_response(str(InvalidCredentialsException), 401)


@router.post("/register")
def register_user(request: CreateUser):
    expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token({"sub": request.email}, expires)
    try:
        user = get_user(request.email)
        return handle_response(UserAlreadyExistsException.message, 403)
    except UserNotFoundException:
        hashed_password = pwd_context.hash(request.password)
        user = CreateUser(email=request.email, password=hashed_password)
        register(user)
        return UserResponse(email=user.email, token=access_token)


@router.post("/auth")
def login(request: CreateUser):
    try:
        user = get_user(request.email)
        if not pwd_context.verify(request.password, user["password"]):  # type: ignore
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect password",
            )

        expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token({"sub": request.email}, expires)

        return UserResponse(email=user["email"], token=access_token)  # type: ignore
    except UserNotFoundException:
        return handle_response(str(UserNotFoundException), 404)
