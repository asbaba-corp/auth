from datetime import timedelta, datetime
from jose import jwt, JWTError
from fastapi import APIRouter, Depends, HTTPException, Header, status
from passlib.context import CryptContext
from src.users.schemas import CreateUser
from src.db.dynamodb.repositories.users_repository import get_user, register

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
route = APIRouter()

SECRET_KEY = "your-secret-key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


def create_access_token(data: dict, expires_delta: timedelta):
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verify_token(authorization: str = Header(...)):
    try:
        scheme, token = authorization.split()
        if scheme.lower() != "bearer":
            raise ValueError("Invalid authentication scheme")

        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except (ValueError, JWTError) as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
        ) from exc
    except Exception as generic_exception:
        # Handle specific errors if needed
        error_message = str(generic_exception)
        raise HTTPException(
            status_code=500, detail=f"Internal server error: {error_message}"
        ) from generic_exception


@route.post("/register")
def register_user(request: CreateUser):
    try:
        user = get_user(request.email)
        print(user)
        if user:
            return {"message": "User already exists"}
        # Hash the password
        hashed_password = pwd_context.hash(request.password)

        user = {
            "email": request.email,
            "password": hashed_password,
        }
        register(user)

        # Generate JWT token
        expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token({"sub": request.email}, expires)

        return {"message": "User registered successfully", "access_token": access_token}
    except Exception as generic_exception:
        # Handle specific errors if needed
        error_message = str(generic_exception)
        raise HTTPException(
            status_code=500, detail=f"Internal server error: {error_message}"
        ) from generic_exception


@route.post("/auth")
def login(request: CreateUser):
    user = get_user(request.email)
    # Verify password

    if not user:
        return {"message": "User doesn't exist"}
    if not pwd_context.verify(request.password, user["password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect password",
        )

    # Generate JWT token
    expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token({"sub": request.email}, expires)

    return {"message": "Login successful", "access_token": access_token}


@route.get("/protec")
def protected_route(payload: dict = Depends(verify_token)):
    return {"message": "This is a protected route", "payload": payload}
