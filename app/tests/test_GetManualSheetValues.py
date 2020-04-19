from app.Domain_Actions.GetManualSheetValues import get_manual_sheet_values
from app.Actions.OpenGoogleWorksheetSession import open_google_worksheet_session
from app.Actions.UpdateCellValue import update_cell_value


class TestGetManualSheetValues:
    def test_values_retrieved_correctly(self, test_state, google_sheet_connection):
        test_state._sessions.update({"GoogleSheets": {"Connection": google_sheet_connection}})
        open_google_worksheet_session(test_state, "IntegrationTest", "TestManual", "daily_manual_worksheet")
        update_cell_value(test_state, "daily_manual_worksheet", "A1", "Item")
        update_cell_value(test_state, "daily_manual_worksheet", "B1", "No.")
        update_cell_value(test_state, "daily_manual_worksheet", "C1", "C")
        update_cell_value(test_state, "daily_manual_worksheet", "D1", "P")
        update_cell_value(test_state, "daily_manual_worksheet", "E1", "V")
        update_cell_value(test_state, "daily_manual_worksheet", "F1", "C")
        update_cell_value(test_state, "daily_manual_worksheet", "G1", "P")
        update_cell_value(test_state, "daily_manual_worksheet", "H1", "V")
        update_cell_value(test_state, "daily_manual_worksheet", "A2", "Manual")
        update_cell_value(test_state, "daily_manual_worksheet", "B2", "3")
        update_cell_value(test_state, "daily_manual_worksheet", "C2", "1")
        update_cell_value(test_state, "daily_manual_worksheet", "D2", "2")
        update_cell_value(test_state, "daily_manual_worksheet", "E2", "3")
        get_manual_sheet_values(test_state)
        expected_values = [["Item", "No.", "C", "P", "V", "C", "P", "V"],
                           ["Manual", "3", "1", "2", "3", "3", "6", "9"]]
        assert test_state.get("daily_manual_worksheet_all_values") == expected_values
