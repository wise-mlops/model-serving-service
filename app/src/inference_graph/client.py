from typing import Optional

from kserve import V1alpha1InferenceGraph
from kserve.constants.constants import KSERVE_V1ALPHA1_VERSION

from app.src.kserve_client import _KServeClient


class InferenceGraphClient(_KServeClient):
    def __init__(self):
        super().__init__()

    def create_inference_graph(self, inference_graph: V1alpha1InferenceGraph,
                               namespace: Optional[str] = None) -> object:
        if namespace:
            return self._client().create_inference_graph(inferencegraph=inference_graph, namespace=namespace)
        return self._client().create_inference_graph(inferencegraph=inference_graph)

    def delete_inference_graph(self, name: str, namespace: Optional[str] = None,
                               version: str = KSERVE_V1ALPHA1_VERSION):
        if namespace:
            self._client().delete_inference_graph(name=name, namespace=namespace, version=version)
        else:
            self._client().delete_inference_graph(name=name, version=version)

    def get_inference_graph(self, name: str, namespace: Optional[str] = None,
                            version: str = KSERVE_V1ALPHA1_VERSION) -> object:
        if namespace:
            return self._client().get_inference_graph(name=name, namespace=namespace, version=version)
        return self._client().get_inference_graph(name=name, version=version)

    def is_inference_graph_ready(self, name: str, namespace: Optional[str] = None,
                                 version: str = KSERVE_V1ALPHA1_VERSION):
        if namespace:
            return self._client().is_ig_ready(name=name, namespace=namespace, version=version)
        return self._client().is_ig_ready(name=name, version=version)

    def wait_inference_graph_ready(self, name: str, namespace: Optional[str] = None,
                                   version: str = KSERVE_V1ALPHA1_VERSION, timeout_seconds: int = 600,
                                   polling_interval: int = 10):
        if namespace:
            self._client().wait_ig_ready(name=name, namespace=namespace, version=version,
                                         timeout_seconds=timeout_seconds, polling_interval=polling_interval)
        else:
            self._client().wait_ig_ready(name=name, version=version, timeout_seconds=timeout_seconds,
                                         polling_interval=polling_interval)
