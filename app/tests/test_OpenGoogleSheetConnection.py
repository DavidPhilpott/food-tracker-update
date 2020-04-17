from app.Actions.OpenGoogleSheetsConnection import open_google_spreadsheet_connection


class TestOpenGoogleSpreadsheetConnection:
    def test_opens_new_connection(self, test_state):
        open_google_spreadsheet_connection(test_state)
        assert test_state.has_session(session_name="GoogleSheetConnection") is True
