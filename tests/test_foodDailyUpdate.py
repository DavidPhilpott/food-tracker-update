import mock

from foodDailyUpdate import main
from foodDailyUpdate import open_google_worksheet
from foodDailyUpdate import get_sheet_cell_value
from foodDailyUpdate import get_all_sheet_values
from foodDailyUpdate import update_cell_value
from foodDailyUpdate import get_current_date
from foodDailyUpdate import assemble_auto_manual_food_items


class TestMain:
    @mock.patch("foodDailyUpdate.update_cell_value")
    @mock.patch("time.sleep")
    def test_update_commands_passed_as_expected(self,
                                                mock_sleep,
                                                mock_update_cell_value,
                                                monkeypatch,
                                                test_state):
        monkeypatch.setenv("google_auth_path", "/home/david/projects/food-tracker-update/GoogleAuth.json")
        main(test_state)
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
        test_state.set({"date_index": "E2"})
        test_state.set({"date_worksheet": "Sheet1"})
        test_state.set({"date_spreadsheet": "IntegrationTest"})
        open_google_worksheet(test_state, "IntegrationTest", "Sheet1")
        get_current_date(test_state)
        assert test_state.get("date_value") == "01-Jan-2000"


class TestAssembleAutoManualFoodItems:
    def test_items_assembled_correctly(self, test_state):
        open_google_worksheet(test_state, "FoodDaily", "Auto")
        open_google_worksheet(test_state, "FoodDaily", "Manual")
        get_all_sheet_values(test_state, "FoodDaily", "Auto")
        get_all_sheet_values(test_state, "FoodDaily", "Manual")

