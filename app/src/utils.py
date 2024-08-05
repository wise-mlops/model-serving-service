from typing import Optional, Dict, List

from kserve import V1beta1ModelFormat, V1beta1LoggerSpec, V1beta1Batcher, V1beta1InferenceServiceSpec, \
    V1beta1InferenceService, V1beta1PredictorSpec, V1beta1ModelSpec, V1beta1TransformerSpec
from kserve.constants.constants import KSERVE_V1BETA1, KSERVE_KIND
from kubernetes.client import V1ContainerPort, V1EnvVar, V1Toleration, V1ObjectMeta, V1ResourceRequirements, V1Container

from app.schemas.inference_service import Resource, ModelFormat, Logger, Env, Toleration, Batcher, \
    InferenceServiceInfo, PredictorSpec, ModelSpec, ResourceRequirements, Port, TransformerSpec, \
    Container


def create_v1beta1_inference_service(name: str, namespace: str, inference_service_info: InferenceServiceInfo):
    return V1beta1InferenceService(
        api_version=KSERVE_V1BETA1,
        kind=KSERVE_KIND,
        metadata=_create_v1_object_meta(
            name=name,
            namespace=namespace,
            annotations=_create_annotations(
                sidecar_inject=inference_service_info.sidecar_inject,
                enable_prometheus_scraping=inference_service_info.enable_prometheus_scraping
            )
        ),
        spec=inference_service_spec
    ) if (inference_service_spec := _create_v1beta1_inference_service_spec(
        predictor_spec=inference_service_info.predictor, transformer_spec=inference_service_info.transformer)) else None


def _create_v1beta1_model_format(model_format: Optional[ModelFormat] = None):
    if not model_format or not model_format.name:
        return None
    return V1beta1ModelFormat(name=model_format.name, version=model_format.version)


def _create_v1_container_port(port: Optional[Port] = None):
    if not port or not all([port.container_port, port.host_ip, port.host_port, port.name, port.protocol]):
        return None
    return V1ContainerPort(container_port=port.container_port, host_ip=port.host_ip, host_port=port.host_port,
                           name=port.name, protocol=port.protocol)


def _create_v1_container_port_list(ports: Optional[List[Port]] = None):
    if not ports:
        return None
    port_list = [v1_container_port for port in ports if (v1_container_port := _create_v1_container_port(port=port))]
    return port_list if port_list else None


def _create_v1beta1_logger_spec(logger: Optional[Logger] = None):
    if not logger or not all([logger.mode, logger.url]):
        return None
    return V1beta1LoggerSpec(mode=logger.mode, url=logger.url)


def _create_v1_env_var(env: Optional[Env] = None):
    if not env or not all([env.name, env.value]):
        return None
    return V1EnvVar(name=env.name, value=env.value, value_from=env.value_from)


def _create_v1_env_var_list(envs: Optional[List[Env]] = None):
    if not envs:
        return None
    env_list = [v1_env_var for env in envs if (v1_env_var := _create_v1_env_var(env=env))]
    return env_list if env_list else None


def _create_v1_toleration(toleration: Optional[Toleration] = None):
    if not toleration or not all([toleration.key, toleration.operator, toleration.value, toleration.effect]):
        return None
    return V1Toleration(key=toleration.key, operator=toleration.operator, value=toleration.value,
                        effect=toleration.effect, toleration_seconds=toleration.toleration_seconds)


def _create_v1_toleration_list(tolerations: Optional[List[Toleration]] = None):
    if not tolerations:
        return None
    toleration_list = [v1_toleration for toleration in tolerations if
                       (v1_toleration := _create_v1_toleration(toleration=toleration))]
    return toleration_list if toleration_list else None


def _create_v1beta1_batcher(batcher: Optional[Batcher] = None):
    if not batcher or all([batcher.max_batch_size is None, batcher.max_latency is None, batcher.timeout is None]):
        return None
    return V1beta1Batcher(max_batch_size=batcher.max_batch_size, max_latency=batcher.max_latency,
                          timeout=batcher.timeout)


def _create_v1_object_meta(name: str, namespace: Optional[str] = None, annotations: Optional[Dict[str, str]] = None):
    return V1ObjectMeta(name=name, namespace=namespace, annotations=annotations)


def _get_resource_dict(resource: Optional[Resource] = None):
    if not resource:
        return None
    resource_dict = {}
    if resource.cpu:
        resource_dict["cpu"] = resource.cpu.strip()
    if resource.memory:
        resource_dict["memory"] = resource.memory.strip()
    if resource.gpu and resource.gpu > 0:
        resource_dict["nvidia.com/gpu"] = str(resource.gpu)
    return resource_dict if resource_dict else None


def _create_v1_resource_requirements(resource_requirements: Optional[ResourceRequirements] = None):
    if not resource_requirements:
        return None
    limits = _get_resource_dict(resource_requirements.limits)
    request = _get_resource_dict(resource_requirements.requests)
    if not limits and not request:
        return None
    return V1ResourceRequirements(limits=limits, requests=request)


def _create_v1_container_list(containers: Optional[List[Container]] = None):
    if not containers:
        return None
    container_list = [v1_container for container in containers if
                      (v1_container := _create_v1_container(container=container))]
    return container_list if container_list else None


def _create_v1_container(container: Optional[Container] = None):
    if not container:
        return None
    return V1Container(image=container.image, image_pull_policy=container.image_pull_policy, name=container.name,
                       command=container.command, args=container.args,
                       ports=_create_v1_container_port_list(ports=container.ports),
                       resources=_create_v1_resource_requirements(resource_requirements=container.resources))


def _create_annotations(
        annotations: Optional[Dict[str, str]] = None,
        sidecar_inject: bool = False,
        enable_prometheus_scraping: bool = False) -> Optional[Dict[str, str]]:
    if annotations is None:
        annotations = {}
    if not sidecar_inject:
        annotations["sidecar.istio.io/inject"] = "false"
    if enable_prometheus_scraping:
        annotations["serving.kserve.io/enable-prometheus-scraping"] = "true"
    return annotations if annotations else None


def _create_v1beta1_inference_service_spec(predictor_spec: PredictorSpec, transformer_spec: Optional[TransformerSpec]):
    return V1beta1InferenceServiceSpec(predictor=predictor,
                                       transformer=_create_v1beta1_transformer_spec(transformer_spec)) if (
        predictor := _create_v1beta1_predictor_spec(predictor_spec=predictor_spec)) else None


def _create_v1beta1_predictor_spec(predictor_spec: PredictorSpec):
    return V1beta1PredictorSpec(model=model_spec, service_account_name=predictor_spec.service_account_name,
                                node_selector=predictor_spec.node_selector, timeout=predictor_spec.timeout,
                                min_replicas=predictor_spec.min_replicas, max_replicas=predictor_spec.max_replicas,
                                scale_target=predictor_spec.scale_target, scale_metric=predictor_spec.scale_metric,
                                canary_traffic_percent=predictor_spec.canary_traffic_percent,
                                batcher=_create_v1beta1_batcher(batcher=predictor_spec.batcher),
                                logger=_create_v1beta1_logger_spec(logger=predictor_spec.logger),
                                tolerations=_create_v1_toleration_list(tolerations=predictor_spec.tolerations)
                                ) if (
        model_spec := _create_v1beta1_model_spec(model_spec=predictor_spec.model)) else None


def _create_v1beta1_model_spec(model_spec: ModelSpec):
    if not model_spec or not all([model_spec.format, model_spec.storage_uri]):
        return None
    return V1beta1ModelSpec(model_format=model_format,
                            storage_uri=model_spec.storage_uri,
                            protocol_version=model_spec.protocol_version,
                            resources=_create_v1_resource_requirements(resource_requirements=model_spec.resources),
                            runtime=model_spec.runtime,
                            runtime_version=model_spec.runtime_version,
                            ports=_create_v1_container_port_list(ports=model_spec.ports),
                            env=_create_v1_env_var_list(envs=model_spec.envs)) if (
        model_format := _create_v1beta1_model_format(model_format=model_spec.format)) else None


def _create_v1beta1_transformer_spec(transformer_spec: Optional[TransformerSpec] = None):
    if not transformer_spec:
        return None
    return V1beta1TransformerSpec(containers=containers, service_account_name=transformer_spec.service_account_name,
                                  node_selector=transformer_spec.node_selector, timeout=transformer_spec.timeout,
                                  min_replicas=transformer_spec.min_replicas,
                                  max_replicas=transformer_spec.max_replicas,
                                  scale_target=transformer_spec.scale_target,
                                  scale_metric=transformer_spec.scale_metric,
                                  canary_traffic_percent=transformer_spec.canary_traffic_percent,
                                  batcher=_create_v1beta1_batcher(batcher=transformer_spec.batcher),
                                  tolerations=_create_v1_toleration_list(tolerations=transformer_spec.tolerations)) if (
        containers := _create_v1_container_list(containers=transformer_spec.containers)) else None
