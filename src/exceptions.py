from typing import Type
from fastapi import HTTPException
from pydantic import BaseModel


class GenericResponse(BaseModel):
    message: str


class DatabaseError(Exception):
    pass


def handle_response(
    message: str, received_status: int, schema: Type[BaseModel] = GenericResponse
):
    if received_status == 200:
        return schema
    statuses = [400, 401, 404, 500, 409]
    if received_status in statuses:
        raise HTTPException(status_code=received_status, detail=message)
    raise HTTPException(status_code=500, detail="Internal Server Error")
