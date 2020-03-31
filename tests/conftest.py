import pytest
from State import State


@pytest.fixture
def test_state():
    test_state = State()
    test_state.set({"google_auth_path": "/home/david/projects/food-tracker-update/GoogleAuth.json"})
    return test_state
