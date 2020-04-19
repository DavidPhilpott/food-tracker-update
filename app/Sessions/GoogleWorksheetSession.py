import time
from gspread.exceptions import APIError


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
        self._state.debug(__name__, f"Opening worksheet session.")
        spreadsheet = self.connection.connection.open_by_key(self.__session_details["spreadsheet_key"])
        self.worksheet = spreadsheet.worksheet(self.__session_details["worksheet_name"])
        return

    def _execute_function(self, function, *args):
        retry_limit = 3
        attempt = 0
        function_complete = False
        result = None
        while not function_complete:
            if attempt > retry_limit:
                raise RuntimeError("Too many retry attempts when running function.")
            try:

                result = function(*args)
                function_complete = True
            except APIError as e:
                if e.response.status_code == 429:
                    self._state.warning(__name__, "Google Sheets API Quota Exceeded.")
                    self._state.warning(__name__, "Sleeping for 100 Seconds.")
                    time.sleep(100)
                    continue
                else:
                    raise

            attempt += 1
        return result

    def _get_cell_value(self, cell_index: str):
        return self.worksheet.acell(cell_index).value

    def get_cell_value(self, cell_index: str):
        self._state.debug(__name__, f"Getting cell value for {cell_index}.")
        return self._execute_function(self._get_cell_value, cell_index)

    def _get_all_sheet_values(self):
        return self.worksheet.get_all_values()

    def get_all_sheet_values(self):
        self._state.debug(__name__, f"Getting all sheet values.")
        return self._execute_function(self._get_all_sheet_values)

    def _update_cell_value(self, cell_index: str, cell_value):
        self.worksheet.update_acell(cell_index, cell_value)
        return

    def update_cell_value(self, cell_index: str, cell_value):
        self._state.debug(__name__, f"Updating cell {cell_index} with value {cell_value}.")
        return self._execute_function(self._update_cell_value, cell_index, cell_value)
