from Sessions.GoogleSheetConnection import GoogleSheetConnection


class TestSessionOpen:
    def test_session_opens(self, test_state):
        connection = GoogleSheetConnection(test_state)
        assert connection.connection is not None
