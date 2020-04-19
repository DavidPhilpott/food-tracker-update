from app.Domain_Actions.CleanUpManualSheet import clean_up_manual_sheet
from app.Actions.OpenGoogleWorksheetSession import open_google_worksheet_session
from app.Actions.UpdateCellValue import update_cell_value
from app.Actions.GetAllSheetValues import get_all_sheet_values


class TestCleanUpManualSheet:
    def test_sheet_cleaned_correctly(self, test_state, google_sheet_connection):
        test_state._sessions.update({'GoogleSheets': {'Connection': google_sheet_connection}})
        open_google_worksheet_session(test_state, "IntegrationTest", "TestManual", 'daily_manual_worksheet')
        update_cell_value(test_state, "daily_manual_worksheet", "A1", "Item")
        update_cell_value(test_state, "daily_manual_worksheet", "B1", "No.")
        update_cell_value(test_state, "daily_manual_worksheet", "C1", "C")
        update_cell_value(test_state, "daily_manual_worksheet", "D1", "P")
        update_cell_value(test_state, "daily_manual_worksheet", "E1", "V")
        update_cell_value(test_state, "daily_manual_worksheet", "F1", "C")
        update_cell_value(test_state, "daily_manual_worksheet", "G1", "P")
        update_cell_value(test_state, "daily_manual_worksheet", "H1", "V")
        update_cell_value(test_state, "daily_manual_worksheet", "A2", "Manual")
        update_cell_value(test_state, "daily_manual_worksheet", "B2", "1")
        update_cell_value(test_state, "daily_manual_worksheet", "B2", "1")
        update_cell_value(test_state, "daily_manual_worksheet", "B2", "2")
        update_cell_value(test_state, "daily_manual_worksheet", "B2", "3")
        expected_values = [["Item", "No.", "C", "P", "V", "C", "P", "V"]]
        get_all_sheet_values(test_state, "daily_manual_worksheet")
        clean_up_manual_sheet(test_state)
        get_all_sheet_values(test_state, "daily_manual_worksheet")
        assert test_state.get("daily_manual_worksheet_all_values") == expected_values
