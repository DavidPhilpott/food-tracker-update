from app.Actions.OpenGoogleSheetsConnection import open_google_spreadsheet_connection


class TestOpenGoogleSpreadsheetConnection:
    def test_opens_new_connection(self, test_state):
        open_google_spreadsheet_connection(test_state)
        result = test_state.get_session("GoogleSheets", "Connection")

        assert test_state.has_session("GoogleSheets", "Connection") is True
