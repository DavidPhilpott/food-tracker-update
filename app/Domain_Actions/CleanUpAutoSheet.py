from app.Actions.UpdateCellValue import update_cell_value


def clean_up_auto_sheet(state) -> None:
    state.info(__name__, 'Wiping daily data from Daily-Auto sheet.')
    state.debug(__name__, 'Getting daily auto worksheet data.')
    auto_sheet_data = state.get('daily_auto_worksheet_all_values')
    if len(auto_sheet_data) > 1:
        state.debug(__name__, "More than one row of data in auto sheet. Blanking sheet's data.")
        for i in range(1, len(auto_sheet_data)):
            state.debug(__name__, f"Blanking data on sheet row '{i+1}'.")
            update_cell_value(state, 'daily_auto_worksheet', f"A{i+1}", "")
            update_cell_value(state, 'daily_auto_worksheet', f"B{i+1}", "")
    state.info(__name__, f"Finished wiping daily auto data.")
    return

