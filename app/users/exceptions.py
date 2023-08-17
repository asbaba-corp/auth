class UserNotFoundException(Exception):
    pass


class UserAlreadyExistsException(Exception):
    message = "User already exists"


class InvalidCredentialsException(Exception):
    pass
