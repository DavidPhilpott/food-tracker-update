from GoogleWorksheetSession import GoogleWorksheetSession


class TestOpenWorksheet:
    def test_open_worksheet_with_connection(self, test_state, google_sheet_connection):
        worksheet_name = 'IntegrationTest'
        session = GoogleWorksheetSession(test_state, google_sheet_connection, worksheet_name)
        assert session is not None
        assert session.connection is not None
