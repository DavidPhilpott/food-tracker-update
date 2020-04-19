from app.Actions.GetAllSheetValues import get_all_sheet_values


def get_manual_sheet_values(state) -> None:
    state.info(__name__, f"Getting all values from Daily-Manual sheet, assuming session 'daily_manual_worksheet'.")
    get_all_sheet_values(state, "daily_manual_worksheet")
    state.info(__name__, f"Finished getting Daily-Manual sheet values.")
    return
