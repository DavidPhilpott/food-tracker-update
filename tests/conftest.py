import pytest
from State import State
from tests.mock_interfaces.mock_EnvVarProvider import MockEnvVarProvider


@pytest.fixture
def test_state():
    test_state = State(env_var_provider=MockEnvVarProvider())
    return test_state
