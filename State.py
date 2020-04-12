import logging
import os
from EnvVarProvider import EnvVarProvider
from AwsParameterStoreProvider import AwsParameterStoreProvider


class State:
    def __init__(self, env_var_provider=None, aws_parameter_store_provider=None):
        self._logger = logging.getLogger(__name__)
        self._logger.setLevel('DEBUG')
        self._state = {}
        self._env_var_provider = env_var_provider
        self._aws_parameter_store_provider = aws_parameter_store_provider
        if env_var_provider is None:
            self._env_var_provider = EnvVarProvider()
        if aws_parameter_store_provider is None:
            self._aws_parameter_store_provider = AwsParameterStoreProvider(self._env_var_provider)

    def get(self, key: str) -> str:
        if not isinstance(key, str):
            raise TypeError(f"Variables must be requested as a string. Requested type is {type(key)}.")
        self.info(f"Getting state value for {key}")
        if key in self._state.keys():
            key_value = self._state[key]
        else:
            self.info(f'{key} not found in local state. Searching OS Env.')
            try:
                key_value = self._env_var_provider.get_var(key)
            except KeyError as exc_info:
                raise
        if type(key_value) == str:
            if key_value.startswith("secret_secure"):
                self.info(f'{key} maps to {key_value}, so fetching from SSM as a secure string.')
                key_value = self._aws_parameter_store_provider.get_secure_string(variable_name=key_value)
            elif key_value.startswith("secret"):
                self.info(f'{key} maps to {key_value}, so fetching from SSM as a regular string.')
                key_value = self._aws_parameter_store_provider.get_non_secure_string(variable_name=key_value)
        return key_value

    def set(self, key_pair: dict):
        if not isinstance(key_pair, dict):
            raise TypeError(f"Variables must be set as a single dict key-pair. Requested type is {type(key_pair)}.")
        if len(key_pair.keys()) != 1:
            raise ValueError(f"Key-pair submitted must be length 1. Current key-pair dict is length {len(key_pair.keys())}.")
        self.info(f"Setting state value for {list(key_pair.keys())[0]}")
        self._state.update(key_pair)

    def info(self, message):
        self._logger.info(message)
