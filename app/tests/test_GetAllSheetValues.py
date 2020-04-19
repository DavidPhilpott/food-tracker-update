from app.Actions.GetAllSheetValues import get_all_sheet_values
from app.Actions.OpenGoogleWorksheetSession import open_google_worksheet_session
from app.Actions.UpdateCellValue import update_cell_value


class TestGetAllSheetValues:
    def test_can_get_all_values_from_test_sheet(self, test_state, google_sheet_connection):
        test_state._sessions.update({"GoogleSheets": {"Connection": google_sheet_connection}})
        open_google_worksheet_session(test_state, "IntegrationTest", "TestAuto", "test_worksheet")
        update_cell_value(test_state, "test_worksheet", "A1", "Item")
        update_cell_value(test_state, "test_worksheet", "B1", "No.")
        update_cell_value(test_state, "test_worksheet", "C1", "Size")
        update_cell_value(test_state, "test_worksheet", "D1", "C")
        update_cell_value(test_state, "test_worksheet", "E1", "P")
        update_cell_value(test_state, "test_worksheet", "F1", "V")
        update_cell_value(test_state, "test_worksheet", "A2", "Auto 1")
        update_cell_value(test_state, "test_worksheet", "B2", "1")
        get_all_sheet_values(test_state, "test_worksheet")
        expected_values = [["Item", "No.", "Size", "C", "P", "V"],
                           ["Auto 1", "1", "Auto 1", "Auto 1", "Auto 1", "Auto 1"]]
        assert test_state.get("test_worksheet_all_values") == expected_values
