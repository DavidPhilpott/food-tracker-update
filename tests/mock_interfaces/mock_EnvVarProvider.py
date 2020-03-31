from tests.mock_variables import mock_variables


class MockEnvVarProvider:
    def __init__(self):
        pass

    def get_var(self, variable_name):
        return mock_variables[variable_name]
