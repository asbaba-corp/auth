from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends
from src.db.connection import get_db

from src.schemas import CreateUser

from src.services import register

route = APIRouter()


@route.post("/auth/register")
def register_user(request: CreateUser, database: Session = Depends(get_db)):
    print(request.email)
    register(database, request, cognito_username="asbaba")
    return {"ok": "ok"}
