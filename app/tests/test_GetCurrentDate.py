from app.Domain_Actions.GetCurrentDate import get_current_date
from app.Actions.OpenGoogleWorksheetSession import open_google_worksheet_session


class TestGetCurrentDate:
    def test_can_fetch_test_date(self, test_state, google_sheet_connection):
        test_state._sessions.update({'GoogleSheets': {"Connection": google_sheet_connection}})
        open_google_worksheet_session(test_state, "IntegrationTest", "TestInfo", 'date_worksheet')
        get_current_date(test_state)
        assert test_state.get("date_value") == "01-Jan-2000"
