class GoogleWorksheetSession:
    def __init__(self, state, connection, spreadsheet_name, worksheet_name):
        self._state = state
        self._state.debug(__name__, f"Initialising session for {spreadsheet_name} - {worksheet_name}")
        self.__session_details = {
            "spreadsheet_key": self._state.get(f"spreadsheet_key_{spreadsheet_name}"),
            "worksheet_name": worksheet_name
        }
        self.connection = connection
        self.__open_worksheet()
        return

    def __open_worksheet(self):
        self._state.debug(__name__, f"Opening worksheet session...")
        spreadsheet = self.connection.connection.open_by_key(self.__session_details["spreadsheet_key"])
        self.worksheet = spreadsheet.worksheet(self.__session_details["worksheet_name"])
        return

    def get_cell_value(self, cell_index: str):
        self._state.debug(__name__, f"Getting cell value for {cell_index}...")
        return self.worksheet.acell(cell_index).value

    def get_all_sheet_values(self):
        self._state.debug(__name__, f"Getting all sheet values...")
        return self.worksheet.get_all_values()

    def update_cell_value(self, cell_index: str, cell_value):
        self._state.debug(__name__, f"Updating cell {cell_index} with value {cell_value}...")
        self.worksheet.update_acell(cell_index, cell_value)
        return
