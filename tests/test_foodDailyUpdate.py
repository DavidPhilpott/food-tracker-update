import mock

from foodDailyUpdate import main
from foodDailyUpdate import open_google_worksheet
from foodDailyUpdate import get_sheet_cell_value
from foodDailyUpdate import get_all_sheet_values
from foodDailyUpdate import update_cell_value


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
        values = get_all_sheet_values(test_state, "IntegrationTest", "Sheet1")
        expected_output = [["A", "B", "C", "Test Value"],
                           ["1", "4", "7", "Test Value 1"],
                           ["2", "5", "8", "Test Value 2"],
                           ["3", "6", "9", "Test Value 3"]]
        assert values == expected_output


class TestUpdateCellValue:
    def test_cell_value_updates_correctly(self, test_state):
        open_google_worksheet(test_state, "IntegrationTest", "PutTest")
        update_cell_value(test_state, "IntegrationTest", "PutTest", "A1", "")
        assert get_sheet_cell_value(test_state, "IntegrationTest", "PutTest", "A1") == ""
        update_cell_value(test_state, "IntegrationTest", "PutTest", "A1", "Test Data")
        assert get_sheet_cell_value(test_state, "IntegrationTest", "PutTest", "A1") == "Test Data"
        update_cell_value(test_state, "IntegrationTest", "PutTest", "A1", "")
        assert get_sheet_cell_value(test_state, "IntegrationTest", "PutTest", "A1") == ""
