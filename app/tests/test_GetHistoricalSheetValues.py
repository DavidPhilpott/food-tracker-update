from app.Domain_Actions.GetHistoricalSheetValues import get_historical_sheet_values
from app.Actions.OpenGoogleWorksheetSession import open_google_worksheet_session


class TestGetHistoricalSheetValues:
    def test_values_retrieved_correctly(self, test_state, google_sheet_connection):
        test_state._sessions.update({"GoogleSheets": {"Connection": google_sheet_connection}})
        open_google_worksheet_session(test_state, "IntegrationTest", "TestHistorical", "historical_core_worksheet")
        get_historical_sheet_values(test_state)
        expected_values = [
            ["Date", "Item", "Number", "Cal", "Prot", "Veg", "Size Details", "Cal", "Prot", "Veg", "Final Cal",
             "Final Prot", "Final Veg"]]
        assert test_state.get("historical_core_worksheet_all_values") == expected_values
