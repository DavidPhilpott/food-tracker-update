from app.Actions.UpdateCellValue import update_cell_value


def clean_up_manual_sheet(state) -> None:
    state.info(__name__, 'Wiping daily data from Daily-Manual sheet.')
    state.debug(__name__, 'Getting daily manual worksheet data.')
    manual_sheet_data = state.get('daily_manual_worksheet_all_values')
    if len(manual_sheet_data) > 1:
        state.debug(__name__, "More than one row of data in manual sheet. Blanking sheet's data.")
        for i in range(1, len(manual_sheet_data)):
            state.debug(__name__, f"Blanking data on sheet row '{i+1}'.")
            update_cell_value(state, 'daily_manual_worksheet', f"A{i+1}", "")
            update_cell_value(state, 'daily_manual_worksheet', f"B{i+1}", "")
            update_cell_value(state, 'daily_manual_worksheet', f"C{i+1}", "")
            update_cell_value(state, 'daily_manual_worksheet', f"D{i+1}", "")
            update_cell_value(state, 'daily_manual_worksheet', f"E{i+1}", "")
    state.info(__name__, f"Finished wiping daily manual data.")
    return

