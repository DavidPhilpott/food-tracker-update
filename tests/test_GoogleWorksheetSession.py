from GoogleWorksheetSession import GoogleWorksheetSession


class TestOpenWorksheet:
    def test_open_worksheet_with_connection(self, test_state, google_sheet_connection):
        spreadsheet_name = 'IntegrationTest'
        worksheet_name = "Sheet1"
        session = GoogleWorksheetSession(test_state, google_sheet_connection, spreadsheet_name, worksheet_name)
        assert session is not None
        assert session.connection is not None
