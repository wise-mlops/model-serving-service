from typing import Any

from pydantic import BaseModel, Field
from starlette import status

from app.config import settings
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
    def success(cls, result):
        instance = cls(result=result)
        instance.result = serialize(instance.result)
        return instance

    @classmethod
    def create(cls, **kwargs):
        instance = cls()
        for key, value in kwargs.items():
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

    def paginate(self, filter_column, query, sort_column, reverse, page_index, page_size):
        return self._search(query=query, target=filter_column)._sort(target=sort_column, reverse=reverse)._paginate(
            page_index=page_index,
            page_size=page_size)

    def _search(self, query, target=None):
        if self.result is None or query is None:
            return self
        if target:
            self.result = [item for item in self.result if query.lower() in str(item[target]).lower()]
        else:
            self.result = [item for item in self.result if
                           any(query.lower() in str(value).lower() for value in item.values())]
        return self

    def _sort(self, target, reverse=False):
        if self.result is None or target is None:
            return self
        self.result = sorted(self.result, key=lambda x: (x[target] is None, x[target]), reverse=reverse)
        return self

    def _paginate(self, page_index, page_size):
        if self.result is None:
            return self
        total_hits = len(self.result)
        if page_size > 0:
            start_index = page_index * page_size
            end_index = start_index + page_size
            self.result = self.result[start_index:end_index]
        self.result = {
            "total_hits": total_hits,
            "result": self.result,
        }
        return self
