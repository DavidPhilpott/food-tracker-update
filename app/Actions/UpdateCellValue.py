def update_cell_value(state, session_name: str, cell_index: str, value: str) -> None:
    state.info(__name__, f"Updating cell value in '{session_name}' at '{cell_index}' to '{value}'.")
    state.debug(__name__, f"Retrieving session '{session_name}'.")
    worksheet = state.get_session('GoogleSheets', session_name)
    state.debug(__name__, f"Updating cell '{cell_index}' to '{value}'.")
    worksheet.update_cell_value(cell_index, value)
    state.info(__name__, f"Finished setting cell value.")
    return
