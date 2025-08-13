class AppError(Exception):
    status_code: int = 400
    code: str = "app_error"

    def __init__(self, detail: str = ""):
        self.detail = detail or self.code

class NotFound(AppError):
    status_code = 404
    code = "not_found"

class Conflict(AppError):
    status_code = 409
    code = "conflict"

