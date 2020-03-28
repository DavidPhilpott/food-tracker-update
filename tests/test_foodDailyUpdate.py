import mock

from foodDailyUpdate import assembleAbsolutePath


class TestAssembleAbsolutePath:
    @mock.patch('os.path.expanduser')
    def test_pathGeneratesCorrectly(self, mocked_expanduser):
        mocked_expanduser.return_value = "/TestHome"
        assert assembleAbsolutePath("Test.py") == "/TestHome/Test.py"
