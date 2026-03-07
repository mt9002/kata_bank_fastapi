from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.modules.account.exceptions import ApiException


def register_exception_handlers(app: FastAPI):

    @app.exception_handler(ApiException)
    async def business_exception_handler(
        request: Request,
        exc: ApiException
    ):
        return JSONResponse(
            status_code=exc.status_code,
            content={
                "title": "business mistake",
                "detail": exc.message
            }
        )

    @app.exception_handler(Exception)
    async def unexpected_exception_handler(
        request: Request,
        exc: Exception
    ):
        return JSONResponse(
            status_code=500,
            content={
                "title": "unexpected error",
                "detail": "An unexpected error occurred. Please contact support.",
                "message": str(exc)
            }
        )