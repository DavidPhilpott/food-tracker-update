import pytest
from app.State import State
from testfixtures import LogCapture


class TestStateInit:
    def test_state_inits_with_logger(self, test_env_var_provider):
        state = State(test_env_var_provider)
        assert state._logging_provider is not None, "State initialised without a logger"


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


class TestLogging:
    def test_info_logs(self, test_state):
        with LogCapture() as log_capture:
            test_state.info("test_name", "test message")
            log_capture.check(
                ("test_name", 'INFO', 'test message')
            )

    def test_warning_logs(self, test_state):
        with LogCapture() as log_capture:
            test_state.warning("test_name", "test message")
            log_capture.check(
                ("test_name", 'WARNING', 'test message')
            )

    def test_debug_logs(self, test_state):
        with LogCapture() as log_capture:
            test_state.debug("test_name", "test message")
            log_capture.check(
                ("test_name", 'DEBUG', 'test message')
            )

    def test_error_logs(self, test_state):
        with LogCapture() as log_capture:
            test_state.error("test_name", "test message")
            log_capture.check(
                ("test_name", 'ERROR', 'test message')
            )


class TestAssembleKeyPathFromArgs:

    def test_no_args_passed_throws_error(self, test_state):
        with pytest.raises(ValueError) as exc_info:
            test_state._assemble_key_list_from_args()
            assert exc_info is not None

    def test_assemble_single_arg(self, test_state):
        assert test_state._assemble_key_list_from_args("GoogleSheets") == ['GoogleSheets']

    def test_assemble_multiple_args(self, test_state):
        assert test_state._assemble_key_list_from_args("GoogleSheets", "TestSpreadsheet", "TestWorksheet") ==\
               ['GoogleSheets', 'TestSpreadsheet', 'TestWorksheet']


class TestSessions:
    def test_can_find_existing_session(self, test_state):
        test_state._sessions.update({"Test Session": "Test Session Value"})
        assert test_state.has_session("Test Session") is True

    def test_cannot_find_non_existing_session(self, test_state):
        assert test_state.has_session("Test Session") is False

    def test_can_find_nested_session(self, test_state):
        test_state._sessions.update({"Test Session": {"Second Layer": "Test Session Value"}})
        assert test_state.has_session("Test Session", "Second Layer")

    def test_cannot_get_non_existing_session(self, test_state):
        with pytest.raises(KeyError) as exc_info:
            test_state.get_session("Test Session")
            assert exc_info is not None

    def test_can_get_existing_session(self, test_state):
        test_state._sessions.update({"Test Session": "Test Session Value"})
        assert test_state.get_session("Test Session") == "Test Session Value"

    def test_can_get_nested_session(self, test_state):
        test_state._sessions.update({"Test Session": {"Second Layer": "Test Session Value"}})
        assert test_state.get_session("Test Session", "Second Layer") == "Test Session Value"

    def test_can_set_session(self, test_state):
        test_state.set_session("Test Session", "Test Session Value")
        assert test_state._sessions == {"Test Session": "Test Session Value"}

    def test_can_set_nested_session(self, test_state):
        test_state.set_session("Test Session", "Second Layer", "Test Session Value")
        assert test_state._sessions == {"Test Session": {"Second Layer": "Test Session Value"}}
