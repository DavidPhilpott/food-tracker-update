from app.Actions.OpenGoogleWorksheetSession import open_google_worksheet_session
from app.Actions.GetAllSheetValues import get_all_sheet_values
from app.Domain_Actions.TransferDailyDataToHistoricalSheet import transfer_daily_data_to_historical_sheet
from app.Actions.UpdateCellValue import update_cell_value


class TestTransferDailyDataToHistoricalSheet:
    def test_values_transfer_correctly(self, test_state, google_sheet_connection):
        test_state._sessions.update({'GoogleSheets': {'Connection': google_sheet_connection}})
        test_state.set({"food_daily_transfer_data": [['Date', 'Item', 'Number', 'Cal', 'Prot', 'Veg'],
                                                     ["01-Jan-2000", "Auto 1", "1", "Auto 1", "Auto 1", "Auto 1"],
                                                     ["01-Jan-2000", "Manual 1", "1", "1", "2", "3"]]})
        expected_values = [["Date", "Item", "Number", "Cal", "Prot", "Veg", "Size Details", "Cal", "Prot", "Veg", "Final Cal", "Final Prot", "Final Veg"],
                           ["01-Jan-2000", "Auto 1", "1", "Auto 1", "Auto 1", "Auto 1", "", "", "", "", "", "", ""],
                           ["01-Jan-2000", "Manual 1", "1", "1", "2", "3", "", "", "", "", "", "", ""]]
        base_values = [["Date", "Item", "Number", "Cal", "Prot", "Veg", "Size Details", "Cal", "Prot", "Veg", "Final Cal", "Final Prot", "Final Veg"]]
        open_google_worksheet_session(test_state, "IntegrationTest", "TestHistorical", 'historical_core_worksheet')
        get_all_sheet_values(test_state, "historical_core_worksheet")
        transfer_daily_data_to_historical_sheet(test_state)
        get_all_sheet_values(test_state, "historical_core_worksheet")
        assert test_state.get("historical_core_worksheet_all_values") == expected_values
        update_cell_value(test_state, "historical_core_worksheet", "A2", "")
        update_cell_value(test_state, "historical_core_worksheet", "B2", "")
        update_cell_value(test_state, "historical_core_worksheet", "C2", "")
        update_cell_value(test_state, "historical_core_worksheet", "D2", "")
        update_cell_value(test_state, "historical_core_worksheet", "E2", "")
        update_cell_value(test_state, "historical_core_worksheet", "F2", "")
        update_cell_value(test_state, "historical_core_worksheet", "A3", "")
        update_cell_value(test_state, "historical_core_worksheet", "B3", "")
        update_cell_value(test_state, "historical_core_worksheet", "C3", "")
        update_cell_value(test_state, "historical_core_worksheet", "D3", "")
        update_cell_value(test_state, "historical_core_worksheet", "E3", "")
        update_cell_value(test_state, "historical_core_worksheet", "F3", "")
        get_all_sheet_values(test_state, "historical_core_worksheet")
        assert test_state.get("historical_core_worksheet_all_values") == base_values
