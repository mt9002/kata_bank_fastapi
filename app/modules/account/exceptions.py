from starlette import status

class ApiException(Exception):
    def __init__(self, message: str, status_code: int):
        super().__init__(message)
        self.message = message
        self.status_code = status_code

class InvalidInitialAmountException(ApiException):
    def __init__(self, message: str):
        super().__init__(message, status.HTTP_400_BAD_REQUEST)
        
class IllegalArgumentAccountException(ApiException):
    def __init__(self, message: str):
        super().__init__(message, status.HTTP_400_BAD_REQUEST)

class AccountAlreadyExistsException(ApiException):
    def __init__(self, message: str):
        super().__init__(message, status.HTTP_409_CONFLICT)

class AccountNotAlreadyExistsException(ApiException):
    def __init__(self, message: str):
        super().__init__(message, status.HTTP_404_NOT_FOUND)

class InvalidTypeTransactionException(ApiException):
    def __init__(self, message: str):
        super().__init__(message, status.HTTP_409_CONFLICT)