from typing import Any, Optional, Union

from pydantic import BaseModel, Field
from starlette import status

from app.config import settings
from app.exceptions.exceptions import ApplicationError
from app.log import Log
from app.utils import serialize
from app.version import VERSION


class APIResponseModel(BaseModel):
    """기본 API 응답 포맷 by AIP Restful API 디자인 가이드

    AI플랫폼팀 API 정식 포맷으로 그대로 사용 권장
    result에는 사용할 응답 포맷을 Typing으로 설정함
    """
    code: int = Field(default=int(f"{settings.SERVICE_CODE}{status.HTTP_200_OK}"))
    message: str = Field(
        default=f"API Response Success ({VERSION})" if Log.is_debug_enable() else "API Response Success"
    )
    result: Any = Field(default={})
    description: str = Field(default="API 응답 성공")

    @classmethod
    def success(cls, result: Any):
        return cls._create(result=result)

    @classmethod
    def create(cls, result: Any, code: Union[str, int], message: Optional[str] = None,
               description: Optional[str] = None):
        len_code = len(str(code))
        if len_code == 3:
            code = int(f"{settings.SERVICE_CODE}{code}")
        elif len_code == 6:
            code = int(code)
        else:
            raise ApplicationError(code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                   message="INTERNAL_SERVER_ERROR",
                                   result="check your response code.")
        return cls._create(code=code, message=message, result=result,
                           description=description)

    @classmethod
    def _create(cls, **kwargs):
        instance = cls()
        for key, value in kwargs.items():
            if value is not None:
                setattr(instance, key, value)
        instance.result = serialize(instance.result)
        return instance

    def to_dict(self):
        return {
            "code": self.code,
            "message": self.message,
            "result": self.result,
            "description": self.description
        }

    def paginate(self, filter_column: Optional[str] = None, search_column: Optional[str] = None,
                 query: Optional[str] = None, sort_column: Optional[str] = None, reverse: Optional[bool] = None,
                 page_index: Optional[int] = None, page_size: int = 0, total_hits: Optional[int] = None):
        return self._search(target=search_column, query=query) \
            ._sort(target=sort_column, reverse=reverse) \
            ._filter(filter_column) \
            ._paginate(page_size=page_size, page_index=page_index, total_hits=total_hits)

    def _filter(self, target: Optional[str] = None):
        if self.result is None:
            return self
        if target and target in self.result.keys():
            self.result = [item for item in self.result[target]]
        return self

    def _search(self, target: Optional[str] = None, query: Optional[str] = None):
        if self.result is None or not query:
            return self
        if target and target in self.result.keys():
            self.result = [item for item in self.result if query.lower() in str(item[target]).lower()]
        else:
            self.result = [item for item in self.result if
                           any(query.lower() in str(value).lower() for value in item.values())]
        return self

    def _sort(self, target: Optional[str] = None, reverse: Optional[bool] = None):
        if self.result is None:
            return self
        if target and target in self.result.keys():
            try:
                self.result = sorted(self.result, key=lambda x: x[target], reverse=bool(reverse))
            except TypeError:
                return self
        return self

    def _paginate(self, page_size: int, page_index: Optional[int] = None,
                  total_hits: Optional[int] = None):
        if self.result is None:
            return self
        if total_hits is None:
            total_hits = len(self.result)
        if page_index is not None and page_size > 0:
            start_index = page_index * page_size
            end_index = start_index + page_size
            if not isinstance(self.result, list):
                return self
            self.result = self.result[start_index:end_index]
        self.result = {
            "total_hits": total_hits,
            "result": self.result,
        }
        return self
