from app.Actions.OpenGoogleWorksheetSession import open_google_worksheet_session


class TestOpenGoogleWorksheetSession:
    def test_session_opens_with_connection(self, test_state, google_sheet_connection):
        test_state._sessions.update({'google_sheets_connection': google_sheet_connection})
        test_spreadsheet_name = 'IntegrationTest'
        test_worksheet_name = 'TestAuto'
        open_google_worksheet_session(state=test_state,
                                      spreadsheet_name=test_spreadsheet_name,
                                      worksheet_name=test_worksheet_name)
        assert test_state.has_session(f"google_worksheet_session_{test_spreadsheet_name}_{test_worksheet_name}")
