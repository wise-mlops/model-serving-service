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
