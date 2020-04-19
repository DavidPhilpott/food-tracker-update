def get_all_sheet_values(state, session_name: str) -> None:
    state.info(__name__, f"Getting all sheet values from session '{session_name}'.")
    state.debug(__name__, f"Fetching session '{session_name}'.")
    worksheet = state.get_session("GoogleSheets", session_name)
    state.debug(__name__, f"Grabbing all sheet values.")
    values = worksheet.get_all_sheet_values()
    state.debug(__name__, f"Values retrieved are: {values}")
    state.debug(__name__, f"Placing values on '{session_name}_all_values'.")
    state.set({f"{session_name}_all_values": values})
    state.info(__name__, f"Finished getting values for sheet on session '{session_name}'.")
    return
