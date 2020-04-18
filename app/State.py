from app.Providers.EnvVarProvider import EnvVarProvider
from app.Providers.AwsParameterStoreProvider import AwsParameterStoreProvider
from app.Providers.LoggingProvider import LoggingProvider


class State:
    def __init__(self, env_var_provider=None, aws_parameter_store_provider=None, logging_provider=None):
        self._state = {}
        self._sessions = {}

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
        return

    def get(self, key: str) -> str:
        if not isinstance(key, str):
            raise TypeError(f"Variables must be requested as a string. Requested type is {type(key)}.")
        self.debug(__name__, f"Fetching state value for '{key}'.")
        if key in self._state.keys():
            key_value = self._state[key]
        else:
            try:
                self.debug(__name__, f"'{key}' not found in local state. Searching OS env.")
                key_value = self._env_var_provider.get_var(key)
            except KeyError as exc_info:
                self.error(__name__, f"Cannot find '{key}' on local state or OS env.")
                raise
        if type(key_value) == str:
            if key_value.startswith("secret_secure"):
                self.debug(__name__, f"'{key}' maps to '{key_value}', so fetching from SSM as a secure string.")
                key_value = self._aws_parameter_store_provider.get_secure_string(variable_name=key_value)
            elif key_value.startswith("secret_pem"):
                self.debug(__name__, f"'{key}' maps to '{key_value}', so fetching from SSM as a PEM key.")
                key_value = self._aws_parameter_store_provider.get_secure_pem_key(variable_name=key_value)
            elif key_value.startswith("secret"):
                self.debug(__name__, f"'{key}' maps to '{key_value}', so fetching from SSM as a regular string.")
                key_value = self._aws_parameter_store_provider.get_non_secure_string(variable_name=key_value)
        self.debug(__name__, f"Found value for '{key}'.")
        return key_value

    def set(self, key_pair: dict):
        if not isinstance(key_pair, dict):
            raise TypeError(f"Variables must be set as a single dict key-pair. Requested type is {type(key_pair)}.")
        if len(key_pair.keys()) != 1:
            raise ValueError(f"Key-pair submitted must be length 1. Current key-pair dict is length {len(key_pair.keys())}.")
        self.debug(__name__, f"Setting state value for '{list(key_pair.keys())[0]}'.")
        self._state.update(key_pair)
        self.debug(__name__, f"Finished setting value for '{list(key_pair.keys())[0]}'.")
        return

    def _assemble_key_list_from_args(self, *args) -> list:
        self.debug(__name__, f"Assembling key list from {args}.")
        if len(args) == 0:
            raise ValueError("No values passed to function. Need at least one value to form key list.")
        key_list = []
        for val in args:
            key_list.append(val)
        self.debug(__name__, f"Finished assembling key list - {key_list}.")
        return key_list

    def _get_session(self, session_keys: list):
        self.debug(__name__, f"Fetching session from state at {session_keys}.")
        structure_to_search = self._sessions
        try:
            for key in session_keys:
                self.debug(__name__, f"Searching sessions at key '{key}'.")
                structure_to_search = structure_to_search[key]
        except KeyError:
            self.debug(__name__, f"Could not find {session_keys} inside sessions.")
            raise
        return structure_to_search

    def get_session(self, *session_args):
        self.debug(__name__, f"Fetching session from state at {session_args}.")
        session_keys = self._assemble_key_list_from_args(*session_args)
        session = self._get_session(session_keys)
        self.debug(__name__, f"Finished fetching session for {session_args}.")
        return session

    def _has_session(self, session_keys: list) -> bool:
        try:
            self._get_session(session_keys)
            self.debug(__name__, f"Found session on state at '{session_keys}'.")
            return True
        except KeyError:
            self.debug(__name__, f"Session '{session_keys}' not found on state.")
            return False

    def has_session(self, *session_args) -> bool:
        self.debug(__name__, f"Checking for session from state at {session_args}.")
        session_keys = self._assemble_key_list_from_args(*session_args)
        return self._has_session(session_keys)

    def _set_session(self, session_keys: list, session_value):
        self.debug(__name__, f"Setting session for {session_keys} to '{session_value}'.")
        dictionary_layer = self._sessions
        for key in session_keys[:-1]:
            self.debug(__name__, f"Current dictionary layer is {dictionary_layer}.")
            self.debug(__name__, f"Moving to dictionary key '{key}'.")
            try:
                dictionary_layer = dictionary_layer[key]
                self.debug(__name__, f"Moved to dictionary key '{key}'.")
            except KeyError:
                self.debug(__name__, f"Could not move to key. Creating default.")
                dictionary_layer.update({key: {}})
                dictionary_layer = dictionary_layer[key]
        final_key = session_keys[-1]
        self.debug(__name__, f"Setting session value '{session_value}' at final layer key '{final_key}'.")
        dictionary_layer[final_key] = session_value
        self.debug(__name__, f"Done setting session for {session_keys} to '{session_value}'.")
        return

    def set_session(self, *session_args):
        self.debug(__name__, f"Setting session for {session_args}.")
        if len(session_args) < 2:
            raise ValueError("Less than two args passed to function. In order to set a session need a path and value.")
        session_value = session_args[-1]
        session_path_args = session_args[:-1]
        session_keys = self._assemble_key_list_from_args(*session_path_args)
        self._set_session(session_keys, session_value)
        return

    def info(self, name, message):
        self._logging_provider.info(name, message)
        return

    def warning(self, name, message):
        self._logging_provider.warning(name, message)
        return

    def debug(self, name, message):
        self._logging_provider.debug(name, message)
        return

    def error(self, name, message):
        self._logging_provider.error(name, message)
        return
