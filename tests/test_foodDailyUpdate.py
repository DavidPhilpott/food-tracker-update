import mock

from foodDailyUpdate import assembleAbsolutePath
from foodDailyUpdate import requestGoogleSheetClient


class TestAssembleAbsolutePath:
    @mock.patch('os.path.expanduser')
    def test_path_generates_correctly(self, mocked_expanduser):
        mocked_expanduser.return_value = "/TestHome"
        assert assembleAbsolutePath("Test.py") == "/TestHome/Test.py"


class TestRequestGoogleSheetClient:
    def test_proper_auth_client_returns(self):
        credentials_path = "/home/david/projects/food-tracker-update/GoogleAuth.json"
        client = requestGoogleSheetClient(credentials_path)
        assert str(type(client)) == "<class 'gspread.client.Client'>"
