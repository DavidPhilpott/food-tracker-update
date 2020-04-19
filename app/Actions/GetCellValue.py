def get_sheet_cell_value(state, session_name: str, index: str) -> str:
    state.info(__name__, f"Getting cell value from session '{session_name}' at '{index}'.")
    state.debug(__name__, f"Retrieving session '{session_name}'.")
    worksheet = state.get_session('GoogleSheets', session_name)
    state.debug(__name__, f"Getting cell index at '{index}'.")
    value = worksheet.get_cell_value(index)
    state.debug(__name__, f"Value retrieved is: {value}")
    state.info(__name__, f"Got cell value. Returning.")
    return value
