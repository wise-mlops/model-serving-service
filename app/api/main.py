from fastapi import APIRouter, Depends
from starlette.responses import JSONResponse

from app.api.dependencies.token import get_token_header
from app.api.routes import inference_service

api_router = APIRouter(dependencies=[Depends(get_token_header)],
                       default_response_class=JSONResponse)

api_router.include_router(inference_service.router)
