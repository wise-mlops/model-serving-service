from typing import Optional

from app.schemas.inference_service import InferenceServiceInfo
from app.src.inference_service import isvc_client
from app.src.inference_service.utils import _get_service_status, _get_creation_timestamp, _get_name, _get_model_format, \
    _get_conditions, _get_namespace, _get_inference_service_host, _get_annotation, _get_service_account, \
    _get_storage_uri, convert_inference_service_url
from app.src.utils import create_v1beta1_inference_service


def create_inference_service(inference_service_info: InferenceServiceInfo, namespace: Optional[str] = None):
    v1beta1_i_svc = create_v1beta1_inference_service(inference_service_info=inference_service_info)
    if v1beta1_i_svc is None:
        return False
    return isvc_client.create(namespace=namespace if namespace else inference_service_info.namespace,
                              inference_service=v1beta1_i_svc)


def get_inference_service(name: Optional[str] = None, namespace: Optional[str] = None):
    return isvc_client.get(name=name, namespace=namespace)


def get_inference_service_parse_detail(name: str, namespace: Optional[str] = None):
    i_svc_detail = get_inference_service(name=name, namespace=namespace)

    detail_metadata_dicts = {
        'name': _get_name(i_svc_detail),
        'overview': {
            'info': {
                'status': _get_service_status(i_svc_detail),
                'api_url': convert_inference_service_url(name),
                'storage_uri': _get_storage_uri(i_svc_detail),
                'model_format': _get_model_format(i_svc_detail),
            },
            'inference_service_conditions': _get_conditions(i_svc_detail),
        },
        'details': {
            'info': {
                'status': _get_service_status(i_svc_detail),
                'name': _get_name(i_svc_detail),
                'namespace': _get_namespace(i_svc_detail),
                'url': _get_inference_service_host(i_svc_detail),
                'annotations': _get_annotation(i_svc_detail),
                'creation_timestamp': _get_creation_timestamp(i_svc_detail),
            },
            'predictor_spec': {
                'storage_uri': _get_storage_uri(i_svc_detail),
                'model_format': _get_model_format(i_svc_detail),
                'service_account': _get_service_account(i_svc_detail)
            }
        },
    }

    return detail_metadata_dicts


def get_inference_service_stat(name: str, namespace: Optional[str] = None):
    i_svc_detail = get_inference_service(name=name, namespace=namespace)
    return _get_service_status(i_svc_detail)


def get_inference_service_list(namespace: Optional[str] = None):
    inference_service_list = get_inference_service(namespace=namespace)
    if isinstance(inference_service_list, dict) and 'items' in inference_service_list:
        return [
            {
                'name': _get_name(item),
                'modelFormat': _get_model_format(item),
                'creationTimestamp': _get_creation_timestamp(item),
                'status': _get_service_status(item)
            } for item in inference_service_list['items']
        ]
    return inference_service_list


def patch_inference_service(inference_service_info: InferenceServiceInfo, name: Optional[str] = None,
                            namespace: Optional[str] = None):
    v1beta1_i_svc = create_v1beta1_inference_service(inference_service_info=inference_service_info)
    if v1beta1_i_svc is None:
        return False
    return isvc_client.patch(name=name if name else inference_service_info.name,
                             namespace=namespace if namespace else inference_service_info.namespace,
                             inference_service=v1beta1_i_svc)


def replace_inference_service(inference_service_info: InferenceServiceInfo, name: Optional[str] = None,
                              namespace: Optional[str] = None):
    v1beta1_i_svc = create_v1beta1_inference_service(inference_service_info=inference_service_info)
    if v1beta1_i_svc is None:
        return False
    return isvc_client.replace(name=name if name else inference_service_info.name,
                               namespace=namespace if namespace else inference_service_info.namespace,
                               inference_service=v1beta1_i_svc)


def delete_inference_service(name: str, namespace: Optional[str] = None):
    return isvc_client.delete(name=name, namespace=namespace)
