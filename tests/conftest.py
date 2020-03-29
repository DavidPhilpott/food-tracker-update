import pytest
from state import State

@pytest.fixture
def test_state():
    test_sate = State()
    return test_sate