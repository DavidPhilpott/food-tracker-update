import mock

from foodDailyUpdate import assembleAbsolutePath
from foodDailyUpdate import request_google_sheet_client
from foodDailyUpdate import main

from gspread import Worksheet

class TestAssembleAbsolutePath:
    @mock.patch('os.path.expanduser')
    def test_path_generates_correctly(self, mocked_expanduser):
        mocked_expanduser.return_value = "/TestHome"
        assert assembleAbsolutePath("Test.py") == "/TestHome/Test.py"


class TestRequestGoogleSheetClient:
    def test_proper_auth_client_returns(self):
        credentials_path = "/home/david/projects/food-tracker-update/GoogleAuth.json"
        client = request_google_sheet_client(credentials_path)
        assert str(type(client)) == "<class 'gspread.client.Client'>"


class TestMain:
    @mock.patch("foodDailyUpdate.assembleAbsolutePath")
    @mock.patch("time.sleep")
    def test_update_commands_passed_as_expected(self,
                                                mock_sleep,
                                                mock_assembleAbsolutePath):
        credentials_path = "/home/david/projects/food-tracker-update/GoogleAuth.json"
        log_file_path = "/home/david/projects/food-tracker-update/FoodDailyTransferLog.txt"
        mock_assembleAbsolutePath.side_effect = [log_file_path, credentials_path]
        main()
        assert True

