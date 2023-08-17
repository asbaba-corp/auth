class UserNotFoundException(Exception):
    message = "User not found"
    status = 404


class UserAlreadyExistsException(Exception):
    message = "User already exists"
    status = 409


class InvalidCredentialsException(Exception):
    message = "Invalid Credentials"
    status = 401
