from datetime import timedelta, datetime
from fastapi import APIRouter, Request
from jose import jwt, JWTError
from passlib.context import CryptContext
from app.exceptions import handle_response  # type: ignore
from app.db.dynamodb.repositories.users_repository import get_user, register
from app.users.config import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES
from app.users.schemas import CreateUser, UserResponse
from app.users.exceptions import (
    UserAlreadyExistsException,
    UserNotFoundException,
    InvalidCredentialsException,
)


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
            return handle_response(
                UserNotFoundException.message, UserNotFoundException.status
            )
        return email
    except JWTError:
        return handle_response(
            InvalidCredentialsException.message, InvalidCredentialsException.status
        )


@router.post("/register")
def register_user(request: CreateUser):
    expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token({"sub": request.email}, expires)
    try:
        user = get_user(request.email)
        return handle_response(
            UserAlreadyExistsException.message, UserAlreadyExistsException.status
        )
    except UserNotFoundException:
        hashed_password = pwd_context.hash(request.password)
        user = CreateUser(email=request.email, password=hashed_password)
        register(user)
        return UserResponse(email=user.email, token=access_token)


@router.post("/login")
def login(request: CreateUser):
    try:
        user = get_user(request.email)
        if not pwd_context.verify(request.password, user["password"]):  # type: ignore
            handle_response(
                InvalidCredentialsException.message, InvalidCredentialsException.status
            )

        expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token({"sub": request.email}, expires)

        return UserResponse(email=user["email"], token=access_token)  # type: ignore
    except UserNotFoundException:
        return handle_response(
            UserNotFoundException.message, UserNotFoundException.status
        )


@router.get("/auth")
def get_current_user_by_token(request: Request):
    try:
        token = request.headers["Authorization"]
        if not token:
            handle_response(
                InvalidCredentialsException.message, InvalidCredentialsException.status
            )

        user = get_current_user(token)
        db_user = get_user(email=user)  # type: ignore
        expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token({"sub": user}, expires)
        return UserResponse(email=db_user["email"], token=access_token)  # type: ignore
    except UserNotFoundException:
        return handle_response(
            UserNotFoundException.message, UserNotFoundException.status
        )
    except KeyError:
        return handle_response("Invalid Authorization Key", 403)
