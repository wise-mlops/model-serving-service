from starlette import status

from app.config import settings
from app.exceptions.exceptions import ApplicationError


class TokenValidationError(ApplicationError):
    """유효하지 않은 토큰 설정"""

    def __init__(self, x_token):
        super().__init__(code=int(f"{settings.SERVICE_CODE}{status.HTTP_401_UNAUTHORIZED}"),
                         message="Invalid x-token header",
                         result={"current_x_token": x_token})
