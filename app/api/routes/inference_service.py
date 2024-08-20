from typing import Optional, List, Any, Dict

from fastapi import APIRouter, Query, Path, Body

from app.schemas.api_response import APIResponseModel
from app.schemas.inference_service import InferenceServiceInfo
from app.src.inference_service import inference_service

router = APIRouter(prefix="/inference-services/{namespace}",
                   tags=["inference-services"])


@router.get("", response_model=APIResponseModel, operation_id="listInferenceServices")
def get_inference_service_list(
        namespace: Optional[str] = Path(..., description='네임스페이스 설정'),
        page_index: Optional[int] = Query(default=None, description='페이지 번호 설정'),
        page_size: Optional[int] = Query(default=None,
                                         description='한 페이지마다 객체 수 설정 (0 이하 값이면 페이징 처리 X)'),
        search_column: Optional[str] = Query(default=None, description='속성 검색 설정'),
        search_keyword: Optional[str] = Query(default=None, description='검색 키워드 설정'),
        sort_column: Optional[str] = Query(default=None, description='정렬 기준 속성 설정'),
        filter_column: Optional[str] = Query(default=None, description='특정 필터 값만 가져오도록 설정'),
        reverse: Optional[bool] = Query(default=None, description='True 오름차순, False 내림차순')
):
    """
    inference service list를 출력합니다.
    """
    return APIResponseModel.success(inference_service.get_inference_service_list(namespace=namespace)).paginate(
        search_column=search_column, query=search_keyword, sort_column=sort_column, reverse=reverse,
        filter_column=filter_column, page_index=page_index, page_size=page_size if page_size is not None else 0,
        total_hits=None)


@router.post("/{name}", response_model=APIResponseModel, operation_id="createInferenceService")
def create_inference_service(
        inference_service_info: InferenceServiceInfo,
        name: str = Path(..., description='inference service명 설정'),
        namespace: str = Path(..., description='네임스페이스 설정')
):
    """
    inference service 만들기\n
        - model format 확인\n
        - inference service 이름 설정\n
            - 이름은 영어 소문자로 시작하고 끝나며, 그 안에는 소문자, 숫자, -만 허용됩니다.
        - minio 경로 설정
    """
    return APIResponseModel.success(
        inference_service.create_inference_service(name=name, namespace=namespace,
                                                   inference_service_info=inference_service_info))


@router.patch("/{name}", response_model=APIResponseModel, operation_id="patchInferenceService")
def patch_inference_service(
        inference_service_info: InferenceServiceInfo,
        name: str = Path(..., description='inference service명 설정'),
        namespace: str = Path(..., description='네임스페이스 설정')
):
    """
    inference service 수정\n
    추후 협의
    """
    return APIResponseModel.success(
        inference_service.patch_inference_service(name=name, namespace=namespace,
                                                  inference_service_info=inference_service_info))


@router.put("/{name}", response_model=APIResponseModel, operation_id="replaceInferenceService")
def replace_inference_service(
        inference_service_info: InferenceServiceInfo,
        name: str = Path(..., description='inference service명 설정'),
        namespace: str = Path(..., description='네임스페이스 설정')
):
    """
    inference service 수정\n
    추후 협의
    """
    return APIResponseModel.success(
        inference_service.replace_inference_service(name=name, namespace=namespace,
                                                    inference_service_info=inference_service_info))


@router.get("/{name}", response_model=APIResponseModel, operation_id="getInferenceService")
def get_inference_service(
        name: str = Path(..., description='inference service명 설정'),
        namespace: str = Path(..., description='네임스페이스 설정')
):
    """
    특정 inference service의 모든 정보를 받아 볼 수 있습니다.
    """
    return APIResponseModel.success(
        inference_service.get_inference_service(name=name, namespace=namespace))


@router.delete("/{name}", response_model=APIResponseModel, operation_id="deleteInferenceService")
def delete_inference_service(
        name: str = Path(..., description='inference service명 설정'),
        namespace: str = Path(..., description='네임스페이스 설정')
):
    """
    특정 inference service 제거
    """
    return APIResponseModel.success(
        inference_service.delete_inference_service(name=name, namespace=namespace))


@router.get("/{name}/detail", response_model=APIResponseModel, operation_id="getInferenceServiceDetail")
def get_inference_service_parse_detail(
        name: str = Path(..., description='inference service명 설정'),
        namespace: str = Path(..., description='네임스페이스 설정')
):
    """
    특정 inference service의 필요한 정보를 받아 볼 수 있습니다.
    """
    return APIResponseModel.success(
        inference_service.get_inference_service_parse_detail(name=name, namespace=namespace))


@router.get("/{name}/stat", response_model=APIResponseModel, operation_id="getInferenceServiceStat")
def get_inference_service_stat(
        name: str = Path(..., description='inference service명 설정'),
        namespace: str = Path(..., description='네임스페이스 설정')
):
    """
    같은 이름의 infernece service가 있는지 확인 할 수 있습니다.
    """
    return APIResponseModel.success(
        inference_service.get_inference_service_stat(name=name, namespace=namespace))


@router.post("/{name}/infer", response_model=APIResponseModel, operation_id="inferenceWithSingleData")
def inference_single(
        name: str = Path(..., description='inference service명 설정'),
        namespace: str = Path(..., description='네임스페이스 설정'),
        data: Any = Body(..., description='테스트 포맷에 맞게 input값을 설정')
):
    """
    inference service를 통해 모델을 테스트 해볼 수 있습니다.\n
        - input값은 각 포맷에 맞게 입력시 output을 받아볼 수 있습니다.\n
        - 단일 데이터 처리
    """
    return APIResponseModel.success(
        inference_service.inference(name=name, namespace=namespace, data=data, multi=False))


@router.post("/{name}/infer-raw", response_model=APIResponseModel, operation_id="inferenceWithRawData")
def inference_raw(
        name: str = Path(..., description='inference service명 설정'),
        namespace: str = Path(..., description='네임스페이스 설정'),
        data: Dict[str, Any] = Body(..., description='테스트 포맷에 맞게 input값을 설정')
):
    """
    inference service를 통해 모델을 테스트 해볼 수 있습니다.\n
        - input값은 각 포맷에 맞게 입력시 output을 받아볼 수 있습니다.\n
        - raw 데이터 처리
    """
    return APIResponseModel.success(
        inference_service.inference(name=name, namespace=namespace, data=data, multi=None))


@router.post("/{name}/infer-multiple", response_model=APIResponseModel, operation_id="inferenceWithMultipleData")
def inference_multiple(
        name: str = Path(..., description='inference service명 설정'),
        namespace: str = Path(..., description='네임스페이스 설정'),
        data: List[Any] = Body(..., description='테스트 포맷에 맞게 input값을 설정')
):
    """
    inference service를 통해 모델을 테스트 해볼 수 있습니다.\n
        - input값은 각 포맷에 맞게 입력시 output을 받아볼 수 있습니다.\n
        - 다중 데이터 처리
    """
    return APIResponseModel.success(
        inference_service.inference(name=name, namespace=namespace, data=data, multi=True))
