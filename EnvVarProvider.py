import os


class EnvVarProvider:
    def __init__(self):
        return

    def get_var(self, variable_name: str):
        return os.environ[variable_name]
