import os


class EnvVarProvider:
    def __init__(self, logging_provider):
        self._logger = logging_provider
        return

    def get_var(self, variable_name: str):
        self._logger.debug(__name__, f"Fetching {variable_name} from OS env...")
        return os.environ[variable_name]
