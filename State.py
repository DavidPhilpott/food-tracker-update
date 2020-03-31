import logging
import os


class State:
    def __init__(self):
        self._logger = logging.getLogger(__name__)
        self._logger.setLevel('DEBUG')
        self._state = {}

    def get(self, key: str) -> str:
        if not isinstance(key, str):
            raise TypeError(f"Variables must be requested as a string. Requested type is {type(key)}.")
        self.info(f"Getting state value for {key}")
        if key in self._state.keys():
            return self._state[key]
        else:
            self.info(f'{key} not found in local state. Searching OS Env.')
            try:
                return os.environ[key]
            except KeyError as exc_info:
                raise

    def set(self, key_pair: dict):
        if not isinstance(key_pair, dict):
            raise TypeError(f"Variables must be set as a single dict key-pair. Requested type is {type(key_pair)}.")
        if len(key_pair.keys()) != 1:
            raise ValueError(f"Key-pair submitted must be length 1. Current key-pair dict is length {len(key_pair.keys())}.")
        self.info(f"Setting state value for {list(key_pair.keys())[0]}")
        self._state.update(key_pair)

    def info(self, message):
        self._logger.info(message)