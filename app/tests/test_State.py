import pytest

from app.State import State


class TestStateInit:
    def test_state_inits_with_logger(self, test_env_var_provider):
        state = State(test_env_var_provider)
        assert state._logger is not None, "State initialised without a logger"


class TestStateGet:
    def test_get_retrieves_value(self, test_env_var_provider):
        test_state = {"Test Var": "Test Val"}
        state = State(test_env_var_provider)
        state._state = test_state
        assert state.get("Test Var") == "Test Val", "State did not retrieve correct value for an existing entry"

    def test_get_variable_from_env_var_if_not_on_state(self, monkeypatch):
        monkeypatch.setenv("DEFAULT_AWS_REGION", "eu-west-1")
        state = State()
        monkeypatch.setenv("Test Var", "Env Var Value")
        assert state.get("Test Var") == 'Env Var Value', "Did not get value from environmental variables"

    def test_get_variable_from_state_preferably(self, monkeypatch, test_env_var_provider):
        test_state = {"Test Var": "Local Var Value"}
        state = State(test_env_var_provider)
        state._state = test_state
        monkeypatch.setenv("Test Var", "Env Var Value")
        assert state.get("Test Var") == 'Local Var Value', "Did not take local state version of variable value"

    def test_get_throw_value_error_for_non_existent_entry(self, test_env_var_provider):
        state = State(test_env_var_provider)
        with pytest.raises(KeyError) as exc_info:
            state.get("Test Var")
        assert exc_info is not None, "State did not throw error when requesting a non-existent entry"

    def test_get_throw_value_error_for_non_string(self, test_env_var_provider):
        state = State(test_env_var_provider)
        with pytest.raises(TypeError) as exc_info:
            state.get(1)
        assert exc_info is not None, "State did not throw error when requesting with a non-string argument"

    def test_get_string_from_parameter_store_if_prefixed_with_secret(self, test_state):
        value = test_state.get("ssm_test_normal_string")
        expected_value = 'Non Secure Test Value'
        assert expected_value == value

    def test_get_secure_string_from_parameter_store_if_prefixed_with_secret_secure(self, test_state):
        value = test_state.get("ssm_secure_test_secure_string")
        expected_value = 'Secure Test Value'
        assert expected_value == value


class TestStateSet:
    def test_set_variable_is_correct(self, test_env_var_provider):
        test_sate = {}
        state = State(test_env_var_provider)
        state._state = test_sate
        state.set({"Test Var": "Test Value"})
        assert state._state == {"Test Var": "Test Value"}, "State did not correct set value"

    def test_set_throws_error_for_multiple_variables(self, test_env_var_provider):
        state = State(test_env_var_provider)
        with pytest.raises(ValueError) as exc_info:
            state.set({"Var1": "Va1", "Var2": "Val2"})
        assert exc_info is not None, "Sate did not throw error when trying to set multiple values at once"

    def test_set_throw_value_error_for_non_dictionary_passed(self, test_env_var_provider):
        state = State(test_env_var_provider)
        with pytest.raises(TypeError) as exc_info:
            state.set("Test Var")
        assert exc_info is not None, "State did not throw error when trying to set a var without passing a dict"


class TestStateInfo:
    def test_message_logged_correctly(self, caplog, test_env_var_provider):
        test_message = "This is an info log"
        state = State(test_env_var_provider)
        state.info(test_message)
        assert len(caplog.messages) == 1, "Expected exactly one log present"
        assert caplog.messages[0] == test_message, "Incorrect log written"

    def test_non_string_logged_correctly(self, caplog, test_env_var_provider):
        test_object = State(test_env_var_provider)
        state = State(test_env_var_provider)
        state.info(test_object)
        assert len(caplog.messages) == 1, "Expected exactly one log present"
        assert caplog.messages[0] == str(test_object), "Incorrect log written"
