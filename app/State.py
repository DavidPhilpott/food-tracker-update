import logging
from app.Providers.EnvVarProvider import EnvVarProvider
from app.Providers.AwsParameterStoreProvider import AwsParameterStoreProvider
from app.Providers.LoggingProvider import LoggingProvider


class State:
    def __init__(self, env_var_provider=None, aws_parameter_store_provider=None, logging_provider=None):
        self._state = {}

        self._logging_provider = logging_provider
        if logging_provider is None:
            self._logging_provider = LoggingProvider()

        self._env_var_provider = env_var_provider
        if env_var_provider is None:
            self._env_var_provider = EnvVarProvider(logging_provider=self._logging_provider)

        self._aws_parameter_store_provider = aws_parameter_store_provider
        if aws_parameter_store_provider is None:
            self._aws_parameter_store_provider = AwsParameterStoreProvider(logging_provider=self._logging_provider,
                                                                           env_var_provider=self._env_var_provider)

    def get(self, key: str) -> str:
        if not isinstance(key, str):
            raise TypeError(f"Variables must be requested as a string. Requested type is {type(key)}.")
        self.debug(__name__, f"Fetching state value for {key}...")
        if key in self._state.keys():
            key_value = self._state[key]
        else:
            try:
                self.debug(__name__, f'{key} not found in local state. Searching OS env...')
                key_value = self._env_var_provider.get_var(key)
            except KeyError as exc_info:
                self.warning(__name__, "Cannot find {key} on local state or OS env.")
                raise
        if type(key_value) == str:
            if key_value.startswith("secret_secure"):
                self.debug(__name__, f'{key} maps to {key_value}, so fetching from SSM as a secure string...')
                key_value = self._aws_parameter_store_provider.get_secure_string(variable_name=key_value)
            elif key_value.startswith("secret_pem"):
                self.debug(__name__, f'{key} maps to {key_value}, so fetching from SSM as a PEM key...')
                key_value = self._aws_parameter_store_provider.get_secure_pem_key(variable_name=key_value)
            elif key_value.startswith("secret"):
                self.debug(__name__, f'{key} maps to {key_value}, so fetching from SSM as a regular string...')
                key_value = self._aws_parameter_store_provider.get_non_secure_string(variable_name=key_value)
        return key_value

    def set(self, key_pair: dict):
        if not isinstance(key_pair, dict):
            raise TypeError(f"Variables must be set as a single dict key-pair. Requested type is {type(key_pair)}.")
        if len(key_pair.keys()) != 1:
            raise ValueError(f"Key-pair submitted must be length 1. Current key-pair dict is length {len(key_pair.keys())}.")
        self.debug(__name__, f"Setting state value for {list(key_pair.keys())[0]}...")
        self._state.update(key_pair)

    def info(self, name, message):
        self._logging_provider.info(name, message)

    def warning(self, name, message):
        self._logging_provider.warning(name, message)

    def debug(self, name, message):
        self._logging_provider.debug(name, message)

    def error(self, name, message):
        self._logging_provider.error(name, message)
