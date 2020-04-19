import mock
from app.foodDailyUpdate import main
from app.State import State


class TestMain:
    @mock.patch("time.sleep")
    @mock.patch("app.foodDailyUpdate.State")
    @mock.patch("app.Actions.UpdateCellValue.update_cell_value")
    def test_update_commands_passed_as_expected(self,
                                                mock_state,
                                                mock_sleep,
                                                monkeypatch,
                                                test_state,
                                                test_env_var_provider):
        mock_state.return_value = State(env_var_provider=test_env_var_provider)
        main()
        assert True
