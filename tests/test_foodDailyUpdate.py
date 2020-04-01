import mock

from foodDailyUpdate import main


class TestMain:
    @mock.patch("foodDailyUpdate.update_cell_value")
    @mock.patch("time.sleep")
    def test_update_commands_passed_as_expected(self,
                                                mock_sleep,
                                                mock_update_cell_value,
                                                monkeypatch,
                                                test_state):
        monkeypatch.setenv("google_auth_path", "/home/david/projects/food-tracker-update/GoogleAuth.json")
        main(test_state)
        assert True
