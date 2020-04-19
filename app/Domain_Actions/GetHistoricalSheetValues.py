from app.Actions.GetAllSheetValues import get_all_sheet_values


def get_historical_sheet_values(state) -> None:
    state.info(__name__, f"Getting all values from Historical-Core sheet, assuming session 'historical_core_worksheet'.")
    get_all_sheet_values(state, "historical_core_worksheet")
    state.info(__name__, f"Finished getting Historical-Core sheet values.")
    return
