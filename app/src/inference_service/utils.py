def _get_metadata(i_svc_detail):
    return i_svc_detail['metadata']


def _get_name(i_svc_detail):
    return _get_metadata(i_svc_detail)['name']


def _get_namespace(i_svc_detail):
    return _get_metadata(i_svc_detail)['namespace']


def _get_creation_timestamp(i_svc_detail):
    return _get_metadata(i_svc_detail)['creationTimestamp']


def _get_annotation(i_svc_detail):
    return _get_metadata(i_svc_detail).get('annotations',
                                           'InferenceService is not ready to receive traffic yet.')


def _get_status(i_svc_detail):
    return i_svc_detail.get('status', 'unknown')


def _get_conditions(i_svc_detail):
    return _get_status(i_svc_detail)['conditions']


def _get_url(i_svc_detail):
    return _get_status(i_svc_detail).get('url', None)


def _get_inference_service_host(i_svc_detail):
    url = _get_url(i_svc_detail)
    if url is None:
        return 'InferenceService is not ready to receive traffic yet.'
    return url.replace("http://", "")


def _get_service_status(i_svc_detail):
    conditions = _get_status(i_svc_detail)
    if conditions != 'unknown':
        return next(
            (cond['status'] for cond in _get_status(i_svc_detail).get('conditions', []) if cond['type'] == 'Ready'),
            'False')
    else:
        return conditions


def _get_predictor_spec(i_svc_detail):
    return i_svc_detail['spec']['predictor']


def _get_service_account(i_svc_detail):
    return _get_predictor_spec(i_svc_detail).get('serviceAccountName',
                                                 'InferenceService is not ready to receive traffic yet.')


def _get_model(i_svc_detail):
    return _get_predictor_spec(i_svc_detail)['model']


def _get_storage_uri(i_svc_detail):
    return _get_model(i_svc_detail)['storageUri']


def _get_model_format(i_svc_detail):
    return _get_model(i_svc_detail)['modelFormat']['name']


def _get_protocol_version(i_svc_detail):
    return _get_model(i_svc_detail)['modelFormat'].get("protocolVersion", "v1")


def convert_inference_service_url(name: str):
    return f"http://211.39.140.216/kserve/{name}/infer"


def _convert_to_v1_form(data, multi: bool = False):
    if multi:
        return {
            "instances": data
        }
    return {
        "instances": [
            data
        ]
    }


def _convert_to_v2_form(data, multi: bool = False):
    if multi:
        inputs = list()
        for i, d in enumerate(data):
            inputs.append({
                "name": f"input_{i}",
                "shape": [len(d), len(d[0])],
                "datatype": "FP32",
                "data": d
            })
        return inputs
    return {
        "inputs": [
            {
                "name": "input",
                "shape": [len(data), len(data[0])],
                "datatype": "FP32",
                "data": data
            }
        ]
    }


def convert_nlp_data(data: dict, task: str):
    formatted_data = None
    if task == 'smr' or task == 'qa' or task == 'query' or task == 'dst':
        formatted_data = {
            "body": data
        }
    return formatted_data
