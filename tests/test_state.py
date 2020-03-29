import pytest

from state import State


class TestStateInit:
    def test_state_inits_with_logger(self):
        state = State()
        assert state._logger is not None, "State initialised without a logger"


class TestStateGet:
    def test_get_retrieves_value(self):
        test_sate = {"Test Var": "Test Val"}
        state = State()
        state._state = test_sate
        assert state.get("Test Var") == "Test Val", "State did not retrieve correct value for an existing entry"

    def test_get_throw_value_error_for_non_existent_entry(self):
        state = State()
        with pytest.raises(KeyError) as exc_info:
            state.get("Test Var")
        assert exc_info is not None, "State did not throw error when requesting a non-existent entry"

    def test_get_throw_value_error_for_non_string(self):
        state = State()
        with pytest.raises(TypeError) as exc_info:
            state.get(1)
        assert exc_info is not None, "State did not throw error when requesting with a non-string argument"


class TestStateSet:
    def test_set_variable_is_correct(self):
        test_sate = {}
        state = State()
        state._state = test_sate
        state.set({"Test Var": "Test Value"})
        assert state._state == {"Test Var": "Test Value"}, "State did not correct set value"

    def test_set_throws_error_for_multiple_variables(selfs):
        state = State()
        with pytest.raises(ValueError) as exc_info:
            state.set({"Var1": "Va1", "Var2": "Val2"})
        assert exc_info is not None, "Sate did not throw error when trying to set multiple values at once"

    def test_set_throw_value_error_for_non_dictionary_passed(self):
        state = State()
        with pytest.raises(TypeError) as exc_info:
            state.set("Test Var")
        assert exc_info is not None, "State did not throw error when trying to set a var without passing a dict"


class TestStateInfo:
    def test_message_logged_correctly(self, caplog):
        test_message = "This is an info log"
        state = State()
        state.info(test_message)
        assert len(caplog.messages) == 1, "Expected exactly one log present"
        assert caplog.messages[0] == test_message, "Incorrect log written"

    def test_non_string_logged_correctly(self, caplog):
        test_object = State()
        state = State()
        state.info(test_object)
        assert len(caplog.messages) == 1, "Expected exactly one log present"
        assert caplog.messages[0] == str(test_object), "Incorrect log written"