import mock, pytest

from foodDailyUpdate import assemble_absolute_path
from foodDailyUpdate import request_google_sheet_client
from foodDailyUpdate import open_google_worksheet
from foodDailyUpdate import get_all_sheet_values
from foodDailyUpdate import main
from State import State

from gspread import Worksheet

class TestAssembleAbsolutePath:
    @mock.patch('os.path.expanduser')
    def test_path_generates_correctly(self, mocked_expanduser):
        mocked_expanduser.return_value = "/TestHome"
        assert assemble_absolute_path("Test.py") == "/TestHome/Test.py"


class TestRequestGoogleSheetClient:
    def test_proper_auth_client_returns(self, monkeypatch):
        credentials_path = "/home/david/projects/food-tracker-update/GoogleAuth.json"
        monkeypatch.setenv("google_auth_path", credentials_path)
        state = State()
        client = request_google_sheet_client(state)
        assert str(type(client)) == "<class 'gspread.client.Client'>"


class TestOpenGoogleWorksheet:
    def test_able_to_open_sheet(self, test_state):
        client = request_google_sheet_client(test_state)
        test_key = '1VWbIiRyZEIVUkoZAGCxX18MTq1eV1tic91V_focnCvw'
        worksheet = open_google_worksheet(google_client=client, sheet_key=test_key)
        assert worksheet is not None


class TestMain:
    @mock.patch("foodDailyUpdate.update_cell_value")
    @mock.patch("foodDailyUpdate.assemble_absolute_path")
    @mock.patch("time.sleep")
    def test_update_commands_passed_as_expected(self,
                                                mock_sleep,
                                                mock_assemble_absolute_path,
                                                mock_update_cell_value,
                                                monkeypatch,
                                                test_state):
        credentials_path = "/home/david/projects/food-tracker-update/GoogleAuth.json"
        monkeypatch.setenv("google_auth_path", "/home/david/projects/food-tracker-update/GoogleAuth.json")
        main(test_state)
        assert True

