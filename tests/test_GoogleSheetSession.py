from GoogleSheetSession import GoogleSheetSession


class TestGoogleSheetSession:
    def test_session_opens(self, test_state):
        session = GoogleSheetSession(test_state)
        assert session.connection is not None
