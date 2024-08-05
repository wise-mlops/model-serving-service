from typing import Optional

from kserve import V1beta1InferenceService
from kserve.constants.constants import KSERVE_V1BETA1_VERSION, KSERVE_V1ALPHA1_VERSION

from app.src.kserve_client import _KServeClient


class InferenceServiceClient(_KServeClient):
    def __init__(self):
        super().__init__()

    def create(self, inference_service: V1beta1InferenceService, namespace: Optional[str] = None, watch: bool = False,
               timeout_seconds: int = 600):
        return self._client().create(inferenceservice=inference_service, namespace=namespace, watch=watch,
                                     timeout_seconds=timeout_seconds)

    def get(self, name: Optional[str] = None, namespace: Optional[str] = None, watch: bool = False,
            timeout_seconds: int = 600, version: str = KSERVE_V1BETA1_VERSION):
        return self._client().get(name=name, namespace=namespace, watch=watch, timeout_seconds=timeout_seconds,
                                  version=version)

    def patch(self, name: str, inference_service: V1beta1InferenceService, namespace: Optional[str] = None,
              watch: bool = False, timeout_seconds: int = 600):
        return self._client().patch(name=name, inferenceservice=inference_service, namespace=namespace, watch=watch,
                                    timeout_seconds=timeout_seconds)

    def replace(self, name: str, inference_service: V1beta1InferenceService, namespace: Optional[str] = None,
                watch: bool = False, timeout_seconds: int = 600):
        return self._client().replace(name=name, inferenceservice=inference_service, namespace=namespace, watch=watch,
                                      timeout_seconds=timeout_seconds)

    def delete(self, name: str, namespace: Optional[str] = None):
        return self._client().delete(name=name, namespace=namespace)

    def is_isvc_ready(self, name: str, namespace: Optional[str] = None, version: str = KSERVE_V1BETA1_VERSION):
        return self._client().is_isvc_ready(name=name, namespace=namespace, version=version)

    def wait_isvc_ready(self, name: Optional[str] = None, namespace: Optional[str] = None, watch: bool = False,
                        timeout_seconds: int = 600, polling_interval: int = 10, version: str = KSERVE_V1BETA1_VERSION):
        self._client().wait_isvc_ready(name=name, namespace=namespace, watch=watch, timeout_seconds=timeout_seconds,
                                       polling_interval=polling_interval, version=version)

    def create_trained_model(self, trained_model, namespace: str):
        self._client().create_trained_model(trainedmodel=trained_model, namespace=namespace)

    def delete_trained_model(self, name: str, namespace: Optional[str] = None, version: str = KSERVE_V1ALPHA1_VERSION):
        return self._client().delete_trained_model(name=name, namespace=namespace, version=version)

    def wait_model_ready(self, inference_service_name: str, model_name: str,
                         inference_service_namespace: Optional[str] = None,
                         inference_service_version: str = KSERVE_V1BETA1_VERSION, cluster_ip: Optional[str] = None,
                         protocol_version: str = "v1", timeout_seconds: int = 600, polling_interval: int = 10):
        self._client().wait_model_ready(service_name=inference_service_name, model_name=model_name,
                                        isvc_namespace=inference_service_namespace,
                                        isvc_version=inference_service_version, cluster_ip=cluster_ip,
                                        protocol_version=protocol_version, timeout_seconds=timeout_seconds,
                                        polling_interval=polling_interval)
