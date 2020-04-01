class GoogleWorksheetSession:
    def __init__(self, state, connection, spreadsheet_name, worksheet_name):
        self.__session_details = {
            "spreadsheet_key": state.get(f"spreadsheet_key_{spreadsheet_name}"),
            "worksheet_name": worksheet_name
        }
        self.connection = connection
        self.__open_worksheet()
        return

    def __open_worksheet(self):
        spreadsheet = self.connection.connection.open_by_key(self.__session_details["spreadsheet_key"])
        self.worksheet = spreadsheet.worksheet(self.__session_details["worksheet_name"])
        return

    def get_cell_value(self, cell_index):
        return self.worksheet.acell(cell_index).value
