from app.Actions.GetCellValue import get_sheet_cell_value
from app.Actions.OpenGoogleWorksheetSession import open_google_worksheet_session


class TestGetSheetCellValue:
    def test_able_to_get_sheet_value(self, test_state, google_sheet_connection):
        test_state._sessions.update({'GoogleSheets': {'Connection': google_sheet_connection}})
        open_google_worksheet_session(test_state, "IntegrationTest", "Sheet1", "Test_Session")
        test_value = get_sheet_cell_value(test_state, 'Test_Session', 'A1')
        assert test_value == "A"
