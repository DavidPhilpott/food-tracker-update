import mock
from app.foodDailyUpdate import main
from app.State import State


class TestMain:
    @mock.patch("app.foodDailyUpdate.update_cell_value")
    @mock.patch("time.sleep")
    @mock.patch("app.foodDailyUpdate.State")
    def test_update_commands_passed_as_expected(self,
                                                mock_state,
                                                mock_sleep,
                                                mock_update_cell_value,
                                                monkeypatch,
                                                test_state,
                                                test_env_var_provider):
        mock_state.return_value = State(env_var_provider=test_env_var_provider)
        main()
        assert True
