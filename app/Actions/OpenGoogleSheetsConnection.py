from app.Sessions.GoogleSheetConnection import GoogleSheetConnection


def open_google_spreadsheet_connection(state) -> None:
    state.info(__name__, "Opening Google Sheets connection.")
    if not state.has_session("GoogleSheets", "Connection"):
        state.debug(__name__, "No existing GoogleSheets connection on state. Opening a new one.")
        session = GoogleSheetConnection(state)
        state.set_session("GoogleSheets", "Connection", session)
        state.info(__name__, "Finished opening Google Sheets connection.")
    else:
        state.info(__name__, "Google Sheets connection already exists on state.")
    return
