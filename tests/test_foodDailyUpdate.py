import mock, pytest

from GoogleSheetConnection import GoogleSheetConnection
from foodDailyUpdate import open_google_worksheet
from foodDailyUpdate import get_all_sheet_values
from foodDailyUpdate import main
from State import State

from gspread import Worksheet


class TestOpenGoogleWorksheet:
    def test_able_to_open_sheet(self, test_state):
        client = GoogleSheetConnection(test_state).connection
        test_key = '1VWbIiRyZEIVUkoZAGCxX18MTq1eV1tic91V_focnCvw'
        worksheet = open_google_worksheet(google_client=client, sheet_key=test_key)
        assert worksheet is not None


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

