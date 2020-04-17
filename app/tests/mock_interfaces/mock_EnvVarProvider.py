from app.tests.mock_variables import mock_variables


class MockEnvVarProvider:
    def __init__(self, logging_provider):
        self._logger = logging_provider
        return

    def get_var(self, variable_name):
        self._logger.debug(__name__, f"Fetching {variable_name} from OS env...")
        return mock_variables[variable_name]