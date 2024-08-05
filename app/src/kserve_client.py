from typing import Optional

from kserve import KServeClient
from kserve.constants.constants import DEFAULT_SA_NAME

from app.config import settings


class _KServeClient:
    def __init__(self):
        self.app_env = settings.APP_ENV
        self.config_path = settings.KUBE_CONFIG_PATH

    def _client(self):
        if self.app_env == "container":
            return KServeClient()
        else:
            return KServeClient(config_file=self.config_path)

    def set_credential(self, storage_type: str, namespace: Optional[str] = None, credentials_file: Optional[str] = None,
                       service_account: str = DEFAULT_SA_NAME, **kwargs):
        return self._client().set_credentials(storage_type=storage_type, namespace=namespace,
                                              credentials_file=credentials_file, service_account=service_account,
                                              **kwargs)
