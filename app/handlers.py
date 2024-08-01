import logging

from fastapi import Request
from fastapi.exceptions import RequestValidationError
from pydantic import ValidationError
from starlette import status
from starlette.exceptions import HTTPException as StarletteHTTPException
from starlette.responses import JSONResponse

from app.config import settings
from app.exceptions.exceptions import ApplicationError
from app.schemas.api_response import APIResponseModel


async def http_exception_handler(request: Request, exc: StarletteHTTPException):
    logging.error(f"{request.client} {request.method} {request.url} → {repr(exc)}")
    status_code = int(f"{settings.SERVICE_CODE}{exc.status_code}")
    if exc.status_code == 404:
        return JSONResponse(
            status_code=200, content=APIResponseModel.create(code=status_code,
                                                             message="Invalid URL. see api-doc `/docs` or `/openapi.json`",
                                                             result={"detail": exc.detail}).to_dict()
        )
    return JSONResponse(
        status_code=200, content=APIResponseModel.create(code=status_code,
                                                         message=exc.detail,
                                                         result={"headers": exc.headers}).to_dict()
    )


async def request_validation_exception_handler(request: Request, exc: RequestValidationError):
    logging.error(f"{request.client} {request.method} {request.url} → {repr(exc)}")
    status_code = int(f"{settings.SERVICE_CODE}{status.HTTP_422_UNPROCESSABLE_ENTITY}")
    return JSONResponse(
        status_code=200, content=APIResponseModel.create(code=status_code,
                                                         message=f"Invalid Request: {exc.errors()[0]['msg']} (type: {exc.errors()[0]['type']}), "
                                                                 f"Check {(exc.errors()[0]['loc'])}",
                                                         result=exc.body).to_dict()
    )


async def validation_exception_handler(request: Request, exc: ValidationError):
    logging.error(f"{request.client} {request.method} {request.url} → {repr(exc)}")
    status_code = int(f"{settings.SERVICE_CODE}{status.HTTP_422_UNPROCESSABLE_ENTITY}")
    return JSONResponse(
        status_code=200, content=APIResponseModel.create(code=status_code,
                                                         message="pydantic model ValidationError 발생",
                                                         result=exc.errors()).to_dict()
    )


async def application_error_handler(request: Request, exc: ApplicationError):
    logging.error(f"{request.client} {request.method} {request.url} → {repr(exc)}")
    return JSONResponse(
        status_code=200, content=APIResponseModel.create(code=exc.code,
                                                         message=exc.message,
                                                         result=exc.result).to_dict()
    )
