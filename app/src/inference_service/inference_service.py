from typing import Optional

from app.schemas.inference_service import InferenceServiceInfo
from app.src.inference_service import isvc_client
from app.src.inference_service.utils import _get_service_status, _get_creation_timestamp, _get_name, _get_model_format
from app.src.utils import create_v1beta1_inference_service


def create_inference_service(inference_service_info: InferenceServiceInfo, namespace: Optional[str] = None):
    v1beta1_i_svc = create_v1beta1_inference_service(inference_service_info=inference_service_info)
    if v1beta1_i_svc is None:
        return False
    return isvc_client.create(namespace=namespace if namespace else inference_service_info.namespace,
                              inference_service=v1beta1_i_svc)


def get_inference_service(name: Optional[str] = None, namespace: Optional[str] = None):
    return isvc_client.get(name=name, namespace=namespace)


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
