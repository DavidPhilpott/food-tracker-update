from app.Sessions.GoogleWorksheetSession import GoogleWorksheetSession


def open_google_worksheet_session(state, spreadsheet_name, worksheet_name):
    state.debug(__name__, f"Opening Google Worksheet session for {spreadsheet_name} - {worksheet_name}.")
    session_name = f"google_worksheet_session_{spreadsheet_name}_{worksheet_name}"
    state.debug(__name__, f"Implied session name is '{session_name}'.")
    if not state.has_session(session_name):
        state.debug(__name__, f"No existing {session_name} on state. Opening a new one.")
        state.debug(__name__, f"Retrieving 'google_sheets_connection' to open session.")
        gsheet_connection = state.get_session("google_sheets_connection")
        session = GoogleWorksheetSession(state=state,
                                         connection=gsheet_connection,
                                         spreadsheet_name=spreadsheet_name,
                                         worksheet_name=worksheet_name)
        state.set_session({session_name: session})
    else:
        state.debug(__name__, f"{session_name} already exists on state.")
    return
