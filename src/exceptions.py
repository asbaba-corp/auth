from fastapi import HTTPException


class DatabaseError(Exception):
    pass


def handle_response(message, received_status):
    if received_status == 200:
        return {"message": message}
    statuses = [400, 401, 404, 500, 409]
    if received_status in statuses:
        raise HTTPException(status_code=received_status, detail=message)
    raise HTTPException(status_code=500, detail="Internal Server Error")
