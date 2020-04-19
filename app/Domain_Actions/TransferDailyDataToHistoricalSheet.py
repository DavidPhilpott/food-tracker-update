from app.Actions.UpdateCellValue import update_cell_value


def transfer_daily_data_to_historical_sheet(state) -> None:
    state.info(__name__, f"Transferring daily data to historical sheet.")
    state.debug(__name__, f"Getting daily transfer data and current historical data.")
    daily_transfer_data = state.get("food_daily_transfer_data")
    historical_data = state.get(f"historical_core_worksheet_all_values")
    state.debug(__name__, f"Writing data to historical sheet.")
    offset = len(historical_data)
    state.debug(__name__, f"Starting at offset '{offset}'.")
    if len(daily_transfer_data) > 1:
        for i in range(1, len(daily_transfer_data)):
            row = i + offset
            state.debug(__name__, f"Writing data row '{i}' to historical sheet row '{row}'.")
            update_cell_value(state, 'historical_core_worksheet', f"A{row}", daily_transfer_data[i][0])
            update_cell_value(state, 'historical_core_worksheet', f"B{row}", daily_transfer_data[i][1])
            update_cell_value(state, 'historical_core_worksheet', f"C{row}", daily_transfer_data[i][2])
            update_cell_value(state, 'historical_core_worksheet', f"D{row}", daily_transfer_data[i][3])
            update_cell_value(state, 'historical_core_worksheet', f"E{row}", daily_transfer_data[i][4])
            update_cell_value(state, 'historical_core_worksheet', f"F{row}", daily_transfer_data[i][5])
    state.info(__name__, f"Finished writing daily transfer data to historical sheet.")
    return