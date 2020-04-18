from app.Sessions.GoogleWorksheetSession import GoogleWorksheetSession


def open_google_worksheet_session(state, spreadsheet_name: str, worksheet_name: str) -> None:
    state.info(__name__, f"Opening Google Worksheet session for {spreadsheet_name} - {worksheet_name}.")
    if not state.has_session("GoogleSheets", spreadsheet_name, worksheet_name):
        state.debug(__name__, f"No existing {spreadsheet_name} - {worksheet_name} on state. Opening a new one.")
        state.debug(__name__, f"Retrieving GoogleSheets connection to open session.")
        gsheet_connection = state.get_session('GoogleSheets', 'Connection')
        session = GoogleWorksheetSession(state=state,
                                         connection=gsheet_connection,
                                         spreadsheet_name=spreadsheet_name,
                                         worksheet_name=worksheet_name)
        state.set_session('GoogleSheets', spreadsheet_name, worksheet_name, session)
        state.info(__name__, f"Finished opening Google Worksheet session for {spreadsheet_name} - {worksheet_name}.")
    else:
        state.info(__name__, f"Google Worksheet session for {spreadsheet_name} - {worksheet_name} already exists on state.")
    return
