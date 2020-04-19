from app.Actions.GetAllSheetValues import get_all_sheet_values


def get_auto_sheet_values(state) -> None:
    state.info(__name__, f"Getting all values from Daily-Auto sheet, assuming session 'daily_auto_worksheet'.")
    get_all_sheet_values(state, "daily_auto_worksheet")
    state.info(__name__, f"Finished getting Daily-Auto sheet values.")
    return
