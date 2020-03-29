import mock

from foodDailyUpdate import assemble_absolute_path
from foodDailyUpdate import request_google_sheet_client
from foodDailyUpdate import open_google_worksheet
from foodDailyUpdate import get_all_sheet_values
from foodDailyUpdate import main

from gspread import Worksheet

class TestAssembleAbsolutePath:
    @mock.patch('os.path.expanduser')
    def test_path_generates_correctly(self, mocked_expanduser):
        mocked_expanduser.return_value = "/TestHome"
        assert assemble_absolute_path("Test.py") == "/TestHome/Test.py"


class TestRequestGoogleSheetClient:
    def test_proper_auth_client_returns(self):
        credentials_path = "/home/david/projects/food-tracker-update/GoogleAuth.json"
        client = request_google_sheet_client(credentials_path)
        assert str(type(client)) == "<class 'gspread.client.Client'>"


class TestOpenGoogleWorksheet:
    def test_able_to_open_sheet(self):
        credentials_path = "/home/david/projects/food-tracker-update/GoogleAuth.json"
        client = request_google_sheet_client(credentials_path)
        test_key = '1rpHCHOHrdWr7LzL4lbc7xxXzuQ_UAIMl26MU2fbzyvU'
        worksheet = open_google_worksheet(google_client=client, sheet_key=test_key)
        assert worksheet is not None


class TestMain:
    @mock.patch("foodDailyUpdate.update_cell_value")
    @mock.patch("foodDailyUpdate.assemble_absolute_path")
    @mock.patch("time.sleep")
    def test_update_commands_passed_as_expected(self,
                                                mock_sleep,
                                                mock_assemble_absolute_path,
                                                mock_update_cell_value):
        credentials_path = "/home/david/projects/food-tracker-update/GoogleAuth.json"
        mock_assemble_absolute_path.side_effect = [credentials_path]
        main()
        assert True

