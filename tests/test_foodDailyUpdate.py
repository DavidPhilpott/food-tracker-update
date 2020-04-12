import mock

from foodDailyUpdate import main
from foodDailyUpdate import open_google_worksheet
from foodDailyUpdate import get_sheet_cell_value
from foodDailyUpdate import get_all_sheet_values
from foodDailyUpdate import update_cell_value
from foodDailyUpdate import get_current_date
from foodDailyUpdate import get_manual_sheet_values
from foodDailyUpdate import get_auto_sheet_values
from foodDailyUpdate import assemble_daily_food_transfer_data
from foodDailyUpdate import get_historical_sheet_values
from foodDailyUpdate import transfer_daily_data_to_historical_sheet
from foodDailyUpdate import clean_up_auto_sheet
from foodDailyUpdate import clean_up_manual_sheet
from tests.mock_interfaces.mock_EnvVarProvider import MockEnvVarProvider
from State import State


class TestMain:
    @mock.patch("foodDailyUpdate.update_cell_value")
    @mock.patch("time.sleep")
    @mock.patch("foodDailyUpdate.State")
    def test_update_commands_passed_as_expected(self,
                                                mock_state,
                                                mock_sleep,
                                                mock_update_cell_value,
                                                monkeypatch,
                                                test_state):
        mock_state.return_value = State(env_var_provider=MockEnvVarProvider())
        main()
        assert True


class TestOpenGoogleWorksheet:
    def test_open_worksheet_is_on_state(self, test_state):
        open_google_worksheet(test_state, "IntegrationTest", "Sheet1")
        test_session = test_state.get("worksheet_IntegrationTestSheet1")
        assert test_session is not None


class TestGetSheetCellValue:
    def test_able_to_retrieve_value(self, test_state):
        open_google_worksheet(test_state, "IntegrationTest", "Sheet1")
        test_value = get_sheet_cell_value(test_state, "IntegrationTest", "Sheet1", "A1")
        assert test_value == "A"


class TestGetAllSheetValues:
    def test_able_to_get_all_values(self, test_state):
        open_google_worksheet(test_state, "IntegrationTest", "Sheet1")
        get_all_sheet_values(test_state, "IntegrationTest", "Sheet1")
        expected_output = [["A", "B", "C", "Test Value", "Date Test"],
                           ["1", "4", "7", "Test Value 1", "01-Jan-2000"],
                           ["2", "5", "8", "Test Value 2", ""],
                           ["3", "6", "9", "Test Value 3", ""]]
        assert test_state.get("worksheet_IntegrationTestSheet1_values") == expected_output


class TestUpdateCellValue:
    def test_cell_value_updates_correctly(self, test_state):
        open_google_worksheet(test_state, "IntegrationTest", "PutTest")
        update_cell_value(test_state, "IntegrationTest", "PutTest", "A1", "")
        assert get_sheet_cell_value(test_state, "IntegrationTest", "PutTest", "A1") == ""
        update_cell_value(test_state, "IntegrationTest", "PutTest", "A1", "Test Data")
        assert get_sheet_cell_value(test_state, "IntegrationTest", "PutTest", "A1") == "Test Data"
        update_cell_value(test_state, "IntegrationTest", "PutTest", "A1", "")
        assert get_sheet_cell_value(test_state, "IntegrationTest", "PutTest", "A1") == ""


class TestGetCurrentDate:
    def test_value_placed_on_state_correctly(self, test_state):
        open_google_worksheet(test_state, "IntegrationTest", "TestInfo")
        get_current_date(test_state)
        assert test_state.get("date_value") == "01-Jan-2000"


class TestAssembleDailyFoodTransferData:
    def test_items_assembled_correctly(self, test_state):
        test_state.set({"date_value": "01-Jan-2000"})
        test_state.set({"worksheet_IntegrationTestTestAuto_values":
                        [["Item", "No.", "Size", "C", "P", "V"], ["Auto 1", "1", "Auto 1", "Auto 1", "Auto 1", "Auto 1"]]})
        test_state.set({"worksheet_IntegrationTestTestManual_values":
                        [["Item", "No.", "C", "P", "V", "C", "P", "V"], ["Manual 1", "1", "1", "2", "3", "1", "2", "3"]]})
        assemble_daily_food_transfer_data(test_state)
        expected_values = [['Date', 'Item', 'Number', 'Cal', 'Prot', 'Veg'],
                           ["01-Jan-2000", "Auto 1", "1", "Auto 1", "Auto 1", "Auto 1"],
                           ["01-Jan-2000", "Manual 1", "1", "1", "2", "3"]]
        assert test_state.get("food_daily_transfer_data") == expected_values


class TestGetManualSheetValues:
    def test_values_retrieved_correctly(self, test_state):
        open_google_worksheet(test_state, "IntegrationTest", "TestManual")
        update_cell_value(test_state, "IntegrationTest", "TestManual", "A1", "Item")
        update_cell_value(test_state, "IntegrationTest", "TestManual", "B1", "No.")
        update_cell_value(test_state, "IntegrationTest", "TestManual", "C1", "C")
        update_cell_value(test_state, "IntegrationTest", "TestManual", "D1", "P")
        update_cell_value(test_state, "IntegrationTest", "TestManual", "E1", "V")
        update_cell_value(test_state, "IntegrationTest", "TestManual", "F1", "C")
        update_cell_value(test_state, "IntegrationTest", "TestManual", "G1", "P")
        update_cell_value(test_state, "IntegrationTest", "TestManual", "H1", "V")
        update_cell_value(test_state, "IntegrationTest", "TestManual", "A2", "Manual")
        update_cell_value(test_state, "IntegrationTest", "TestManual", "B2", "3")
        update_cell_value(test_state, "IntegrationTest", "TestManual", "C2", "1")
        update_cell_value(test_state, "IntegrationTest", "TestManual", "D2", "2")
        update_cell_value(test_state, "IntegrationTest", "TestManual", "E2", "3")
        get_manual_sheet_values(test_state)
        expected_values = [["Item", "No.", "C", "P", "V", "C", "P", "V"],
                           ["Manual", "3", "1", "2", "3", "3", "6", "9"]]
        assert test_state.get("worksheet_IntegrationTestTestManual_values") == expected_values


class TestGetAutoSheetValues:
    def test_values_retrieved_correctly(self, test_state):
        open_google_worksheet(test_state, "IntegrationTest", "TestAuto")
        update_cell_value(test_state, "IntegrationTest", "TestAuto", "A1", "Item")
        update_cell_value(test_state, "IntegrationTest", "TestAuto", "B1", "No.")
        update_cell_value(test_state, "IntegrationTest", "TestAuto", "C1", "Size")
        update_cell_value(test_state, "IntegrationTest", "TestAuto", "D1", "C")
        update_cell_value(test_state, "IntegrationTest", "TestAuto", "E1", "P")
        update_cell_value(test_state, "IntegrationTest", "TestAuto", "F1", "V")
        update_cell_value(test_state, "IntegrationTest", "TestAuto", "A2", "Auto 1")
        update_cell_value(test_state, "IntegrationTest", "TestAuto", "B2", "1")
        get_auto_sheet_values(test_state)
        expected_values = [["Item", "No.", "Size", "C", "P", "V"],
                           ["Auto 1", "1", "Auto 1", "Auto 1", "Auto 1", "Auto 1"]]
        assert test_state.get("worksheet_IntegrationTestTestAuto_values") == expected_values


class TestGetHistoricalSheetValues:
    def test_values_retrieved_correctly(self, test_state):
        open_google_worksheet(test_state, "IntegrationTest", "TestHistorical")
        get_historical_sheet_values(test_state)
        expected_values = [["Date", "Item", "Number", "Cal", "Prot", "Veg", "Size Details", "Cal", "Prot", "Veg", "Final Cal", "Final Prot", "Final Veg"]]
        assert test_state.get("worksheet_IntegrationTestTestHistorical_values") == expected_values


class TestTransferDailyDataToHistoricalSheet:
    def test_values_transfer_correctly(self, test_state):
        test_state.set({"food_daily_transfer_data": [['Date', 'Item', 'Number', 'Cal', 'Prot', 'Veg'],
                                                     ["01-Jan-2000", "Auto 1", "1", "Auto 1", "Auto 1", "Auto 1"],
                                                     ["01-Jan-2000", "Manual 1", "1", "1", "2", "3"]]})
        expected_values = [["Date", "Item", "Number", "Cal", "Prot", "Veg", "Size Details", "Cal", "Prot", "Veg", "Final Cal", "Final Prot", "Final Veg"],
                           ["01-Jan-2000", "Auto 1", "1", "Auto 1", "Auto 1", "Auto 1", "", "", "", "", "", "", ""],
                           ["01-Jan-2000", "Manual 1", "1", "1", "2", "3", "", "", "", "", "", "", ""]]
        base_values = [["Date", "Item", "Number", "Cal", "Prot", "Veg", "Size Details", "Cal", "Prot", "Veg", "Final Cal", "Final Prot", "Final Veg"]]
        open_google_worksheet(test_state, "IntegrationTest", "TestHistorical")
        get_all_sheet_values(test_state, "IntegrationTest", "TestHistorical")
        transfer_daily_data_to_historical_sheet(test_state)
        get_all_sheet_values(test_state, "IntegrationTest", "TestHistorical")
        assert test_state.get("worksheet_IntegrationTestTestHistorical_values") == expected_values
        update_cell_value(test_state, "IntegrationTest", "TestHistorical", "A2", "")
        update_cell_value(test_state, "IntegrationTest", "TestHistorical", "B2", "")
        update_cell_value(test_state, "IntegrationTest", "TestHistorical", "C2", "")
        update_cell_value(test_state, "IntegrationTest", "TestHistorical", "D2", "")
        update_cell_value(test_state, "IntegrationTest", "TestHistorical", "E2", "")
        update_cell_value(test_state, "IntegrationTest", "TestHistorical", "F2", "")
        update_cell_value(test_state, "IntegrationTest", "TestHistorical", "A3", "")
        update_cell_value(test_state, "IntegrationTest", "TestHistorical", "B3", "")
        update_cell_value(test_state, "IntegrationTest", "TestHistorical", "C3", "")
        update_cell_value(test_state, "IntegrationTest", "TestHistorical", "D3", "")
        update_cell_value(test_state, "IntegrationTest", "TestHistorical", "E3", "")
        update_cell_value(test_state, "IntegrationTest", "TestHistorical", "F3", "")
        get_all_sheet_values(test_state, "IntegrationTest", "TestHistorical")
        assert test_state.get("worksheet_IntegrationTestTestHistorical_values") == base_values


class TestCleanUpAutoSheet:
    def test_sheet_cleaned_correctly(self, test_state):
        open_google_worksheet(test_state, "IntegrationTest", "TestAuto")
        update_cell_value(test_state, "IntegrationTest", "TestAuto", "A1", "Item")
        update_cell_value(test_state, "IntegrationTest", "TestAuto", "B1", "No.")
        update_cell_value(test_state, "IntegrationTest", "TestAuto", "C1", "Size")
        update_cell_value(test_state, "IntegrationTest", "TestAuto", "D1", "C")
        update_cell_value(test_state, "IntegrationTest", "TestAuto", "E1", "P")
        update_cell_value(test_state, "IntegrationTest", "TestAuto", "F1", "V")
        update_cell_value(test_state, "IntegrationTest", "TestAuto", "A2", "Auto 1")
        update_cell_value(test_state, "IntegrationTest", "TestAuto", "B2", "1")
        expected_values = [["Item", "No.", "Size", "C", "P", "V"]]
        get_all_sheet_values(test_state, "IntegrationTest", "TestAuto")
        clean_up_auto_sheet(test_state)
        get_all_sheet_values(test_state, "IntegrationTest", "TestAuto")
        assert test_state.get("worksheet_IntegrationTestTestAuto_values") == expected_values



class TestCleanUpManualSheet:
    def test_sheet_cleaned_correctly(self, test_state):
        open_google_worksheet(test_state, "IntegrationTest", "TestManual")
        update_cell_value(test_state, "IntegrationTest", "TestManual", "A1", "Item")
        update_cell_value(test_state, "IntegrationTest", "TestManual", "B1", "No.")
        update_cell_value(test_state, "IntegrationTest", "TestManual", "C1", "C")
        update_cell_value(test_state, "IntegrationTest", "TestManual", "D1", "P")
        update_cell_value(test_state, "IntegrationTest", "TestManual", "E1", "V")
        update_cell_value(test_state, "IntegrationTest", "TestManual", "F1", "C")
        update_cell_value(test_state, "IntegrationTest", "TestManual", "G1", "P")
        update_cell_value(test_state, "IntegrationTest", "TestManual", "H1", "V")
        update_cell_value(test_state, "IntegrationTest", "TestManual", "A2", "Manual")
        update_cell_value(test_state, "IntegrationTest", "TestManual", "B2", "1")
        update_cell_value(test_state, "IntegrationTest", "TestManual", "B2", "1")
        update_cell_value(test_state, "IntegrationTest", "TestManual", "B2", "2")
        update_cell_value(test_state, "IntegrationTest", "TestManual", "B2", "3")
        expected_values = [["Item", "No.", "C", "P", "V", "C", "P", "V"]]
        get_all_sheet_values(test_state, "IntegrationTest", "TestManual")
        clean_up_manual_sheet(test_state)
        get_all_sheet_values(test_state, "IntegrationTest", "TestManual")
        assert test_state.get("worksheet_IntegrationTestTestManual_values") == expected_values
