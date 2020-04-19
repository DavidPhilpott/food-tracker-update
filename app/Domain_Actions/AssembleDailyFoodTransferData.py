def assemble_daily_food_transfer_data(state) -> None:
    state.info(__name__, f"Assembling daily data to be transferred.")
    state.debug(__name__, f"Fetching date and daily-auto, daily-manual worksheet values.")
    current_date = state.get("date_value")
    auto_data = state.get(f"daily_auto_worksheet_all_values")
    manual_data = state.get(f"daily_manual_worksheet_all_values")
    state.debug(__name__, "Creating transfer data.")
    transfer_data = [["Date", "Item", "Number", "Cal", "Prot", "Veg"]]
    state.debug(__name__, "Adding auto sheet data.")
    for i in range(1, len(auto_data)):
        transfer_data.append([current_date, auto_data[i][0], auto_data[i][1], '', '', ''])
    state.debug(__name__, f"Transfer data is now: {transfer_data}")
    state.debug(__name__, "Adding manual sheet data.")
    for i in range(1, len(manual_data)):
        transfer_data.append([current_date, manual_data[i][0], manual_data[i][1], manual_data[i][2], manual_data[i][3], manual_data[i][4]])
    state.debug(__name__, f"Transfer data is now: {transfer_data}")
    state.debug(__name__, "Replacing ' -' entries with ''.")
    for i in range(1, len(transfer_data)):
        for j in range(1, len(transfer_data[0])):
            if transfer_data[i][j] == ' -':
                transfer_data[i][j] = ''
    state.debug(__name__, f"Transfer data is now: {transfer_data}")
    state.debug(__name__, f"Place transfer data on state.")
    state.set({"food_daily_transfer_data": transfer_data})
    return
