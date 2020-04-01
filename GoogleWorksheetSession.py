class GoogleWorksheetSession:
    def __init__(self, state, connection, worksheet_name):
        self.__session_details = {
            "worksheet_key": state.get(f"worksheet_key_{worksheet_name}")
        }
        self.connection = connection
        self.__open_worksheet()
        return

    def __open_worksheet(self):
        worksheet = self.connection.connection.open_by_key(self.__session_details["worksheet_key"])
        self.worksheet = worksheet
        return
