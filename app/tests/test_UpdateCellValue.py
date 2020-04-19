from app.Actions.UpdateCellValue import update_cell_value
from app.Actions.OpenGoogleWorksheetSession import open_google_worksheet_session
from app.Actions.GetCellValue import get_sheet_cell_value


class TestUpdateCellValue:
    def test_able_to_update_cell_value(self, test_state, google_sheet_connection):
        test_state._sessions.update({'GoogleSheets': {'Connection': google_sheet_connection}})
        open_google_worksheet_session(test_state, 'IntegrationTest', 'PutTest', 'Test_Session')
        update_cell_value(test_state, "Test_Session", "A1", "", )
        assert get_sheet_cell_value(test_state, "Test_Session", "A1") == ""
        update_cell_value(test_state, "Test_Session", "A1", "Test Data")
        assert get_sheet_cell_value(test_state, "Test_Session", "A1") == "Test Data"
        update_cell_value(test_state, "Test_Session", "A1", "")
        assert get_sheet_cell_value(test_state, "Test_Session", "A1") == ""
