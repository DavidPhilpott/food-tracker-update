from app.Actions.GetCellValue import get_sheet_cell_value


def get_current_date(state) -> None:
    state.info(__name__, "Getting current date.")
    state.debug(__name__, "Fetching date index variable.")
    date_index = state.get("date_index")
    state.debug(__name__, "Fetching date worksheet session")
    date_value = get_sheet_cell_value(state, "date_worksheet", date_index)
    state.debug(__name__, "Setting date value on state.")
    state.set({"date_value": date_value})
    state.info(__name__, "Finished getting current date.")
    return
