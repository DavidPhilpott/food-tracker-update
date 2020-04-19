import mock

from app.foodDailyUpdate import main
from app.foodDailyUpdate import open_google_worksheet
from app.foodDailyUpdate import get_sheet_cell_value
from app.foodDailyUpdate import get_all_sheet_values
from app.foodDailyUpdate import update_cell_value
from app.foodDailyUpdate import get_current_date
from app.foodDailyUpdate import get_manual_sheet_values
from app.foodDailyUpdate import get_auto_sheet_values
from app.foodDailyUpdate import assemble_daily_food_transfer_data
from app.foodDailyUpdate import get_historical_sheet_values
from app.foodDailyUpdate import transfer_daily_data_to_historical_sheet
from app.foodDailyUpdate import clean_up_auto_sheet
from app.foodDailyUpdate import clean_up_manual_sheet
from app.tests.mock_interfaces.mock_EnvVarProvider import MockEnvVarProvider
from app.Actions.OpenGoogleWorksheetSession import open_google_worksheet_session
from app.Actions.OpenGoogleSheetsConnection import open_google_spreadsheet_connection

from app.State import State


class TestMain:
    @mock.patch("app.foodDailyUpdate.update_cell_value")
    @mock.patch("time.sleep")
    @mock.patch("app.foodDailyUpdate.State")
    def test_update_commands_passed_as_expected(self,
                                                mock_state,
                                                mock_sleep,
                                                mock_update_cell_value,
                                                monkeypatch,
                                                test_state,
                                                test_env_var_provider):
        mock_state.return_value = State(env_var_provider=test_env_var_provider)
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
