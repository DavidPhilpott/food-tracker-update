from app.Sessions.GoogleWorksheetSession import GoogleWorksheetSession


class TestOpenWorksheet:
    def test_open_worksheet_with_connection(self, test_state, google_sheet_connection):
        spreadsheet_name = 'IntegrationTest'
        worksheet_name = "Sheet1"
        session = GoogleWorksheetSession(test_state, google_sheet_connection, spreadsheet_name, worksheet_name)
        assert session is not None
        assert session.connection is not None


class TestReadCellValue:
    def test_read_cell_value_from_sheet(self, test_worksheet_session):
        value = test_worksheet_session.get_cell_value("D1")
        assert value == 'Test Value'


class TestGetAllSheetValues:
    def test_read_all_values_from_sheet(self, test_worksheet_session):
        values = test_worksheet_session.get_all_sheet_values()
        expected_output = [["A", "B", "C", "Test Value", "Date Test"],
                           ["1", "4", "7", "Test Value 1", "01-Jan-2000"],
                           ["2", "5", "8", "Test Value 2", ""],
                           ["3", "6", "9", "Test Value 3", ""]]
        assert values == expected_output


class TestUpdateCellValue:
    def test_successfully_update_value(self, test_worksheet_write_session):
        test_worksheet_write_session.update_cell_value("A1", "")
        assert test_worksheet_write_session.get_cell_value("A1") == ""
        test_worksheet_write_session.update_cell_value("A1", "Test Data")
        assert test_worksheet_write_session.get_cell_value("A1") == "Test Data"
        test_worksheet_write_session.update_cell_value("A1", "")
        assert test_worksheet_write_session.get_cell_value("A1") == ""
