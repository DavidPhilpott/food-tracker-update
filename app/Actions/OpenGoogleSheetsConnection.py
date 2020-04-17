from app.Sessions.GoogleSheetConnection import GoogleSheetConnection


def open_google_spreadsheet_connection(state):
    state.debug(__name__, "Opening Google Sheet connection.")
    if not state.has_session("GoogleSheetConnection"):
        state.debug(__name__, "No existing GoogleSheetConnection on state. Opening a new one.")
        session = GoogleSheetConnection(state)
        state.set_session({"GoogleSheetConnection": session})
    else:
        state.debug(__name__, "GoogleSheetSession already exists on state.")
    return
