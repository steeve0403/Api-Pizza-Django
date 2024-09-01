from ninja.errors import HttpError


class NotFoundError(HttpError):
    def __init__(self, detail: str = "Resource not found"):
        super().__init__(status_code=404, detail=detail)


class BadRequestError(HttpError):
    def __init__(self, detail: str = "Bad request"):
        super().__init__(status_code=400, detail=detail)


class UnauthorizedError(HttpError):
    def __init__(self, detail: str = "Unauthorized"):
        super().__init__(status_code=401, detail=detail)


class ForbiddenError(HttpError):
    def __init__(self, detail: str = "Forbidden"):
        super().__init__(status_code=403, detail=detail)


def global_exception_handler(request, exc):
    if isinstance(exc, HttpError):
        return exc.to_response()
    return {"detail": "An error has occurred : " + str(exc)}, 500
