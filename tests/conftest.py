import pytest
from State import State
from tests.mock_interfaces.mock_EnvVarProvider import MockEnvVarProvider
from GoogleSheetConnection import GoogleSheetConnection


@pytest.fixture
def test_state():
    test_state = State(env_var_provider=MockEnvVarProvider())
    return test_state


@pytest.fixture
def google_sheet_connection(test_state):
    google_sheet_connection = GoogleSheetConnection(test_state)
    return google_sheet_connection
