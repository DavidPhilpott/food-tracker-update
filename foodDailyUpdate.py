import time
from State import State
from GoogleSheetConnection import GoogleSheetConnection
from GoogleWorksheetSession import GoogleWorksheetSession


def update_cell_value(state, spreadsheet_name: str, worksheet_name: str, cell_index: str, value: str) -> None:
    worksheet = state.get(f"worksheet_{spreadsheet_name}{worksheet_name}")
    worksheet.update_cell_value(cell_index, value)
    return


def open_google_worksheet(state, spreadsheet_name: str, worksheet_name: str) -> None:
    worksheet = GoogleWorksheetSession(state, GoogleSheetConnection(state), spreadsheet_name, worksheet_name)
    state.set({f"worksheet_{spreadsheet_name}{worksheet_name}": worksheet})
    return


def get_sheet_cell_value(state, spreadsheet_name: str, worksheet_name: str, index: str) -> str:
    worksheet = state.get(f"worksheet_{spreadsheet_name}{worksheet_name}")
    return worksheet.get_cell_value(index)


def get_all_sheet_values(state, spreadsheet_name: str, worksheet_name: str):
    worksheet = state.get(f"worksheet_{spreadsheet_name}{worksheet_name}")
    worksheet_values = worksheet.get_all_sheet_values()
    state.set({f"worksheet_{spreadsheet_name}{worksheet_name}_values": worksheet_values})
    return


def get_current_date(state) -> None:
    date_index = state.get("date_index")
    spreadsheet_name = state.get("date_spreadsheet")
    worksheet_name = state.get("date_worksheet")
    date_value = get_sheet_cell_value(state, spreadsheet_name, worksheet_name, date_index)
    state.set({"date_value": date_value})
    return


def get_manual_sheet_values(state) -> None:
    manual_spreadsheet_name = state.get("daily_manual_spreadsheet_name")
    manual_worksheet_name = state.get("daily_manual_worksheet_name")
    get_all_sheet_values(state, manual_spreadsheet_name, manual_worksheet_name)
    return


def get_auto_sheet_values(state) -> None:
    auto_spreadsheet_name = state.get("daily_auto_spreadsheet_name")
    auto_worksheet_name = state.get("daily_auto_worksheet_name")
    get_all_sheet_values(state, auto_spreadsheet_name, auto_worksheet_name)
    return


def get_historical_sheet_values(state) -> None:
    historical_spreadsheet_name = state.get("core_spreadsheet_name")
    historical_worksheet_name = state.get("core_worksheet_name")
    get_all_sheet_values(state, historical_spreadsheet_name, historical_worksheet_name)
    return


def assemble_daily_food_transfer_data(state) -> None:
    current_date = state.get("date_value")
    auto_spreadsheet_name = state.get("daily_auto_spreadsheet_name")
    auto_worksheet_name = state.get("daily_auto_worksheet_name")
    auto_data = state.get(f"worksheet_{auto_spreadsheet_name}{auto_worksheet_name}_values")
    manual_spreadsheet_name = state.get("daily_manual_spreadsheet_name")
    manual_worksheet_name = state.get("daily_manual_worksheet_name")
    manual_data = state.get(f"worksheet_{manual_spreadsheet_name}{manual_worksheet_name}_values")
    transfer_data = [["Date", "Item", "Number", "Cal", "Prot", "Veg"]]
    for i in range(1, len(auto_data)):
        transfer_data.append([current_date, auto_data[i][0], auto_data[i][1], auto_data[i][3], auto_data[i][4], auto_data[i][5]])
    for i in range(1, len(manual_data)):
        transfer_data.append([current_date, manual_data[i][0], manual_data[i][1], manual_data[i][2], manual_data[i][3], manual_data[i][4]])
    state.set({"food_daily_transfer_data": transfer_data})
    return


def transfer_daily_data_to_historical_sheet(state) -> None:
    daily_transfer_data = state.get("food_daily_transfer_data")
    historical_spreadsheet = state.get('core_spreadsheet_name')
    historical_worksheet = state.get('core_worksheet_name')
    historical_data = state.get(f"worksheet_{historical_spreadsheet}{historical_worksheet}_values")
    offset = len(historical_data)
    if len(daily_transfer_data) > 1:
        for i in range(1, len(daily_transfer_data)):
            row = i + offset
            update_cell_value(state, historical_spreadsheet, historical_worksheet, f"A{row}", daily_transfer_data[i][0])
            update_cell_value(state, historical_spreadsheet, historical_worksheet, f"B{row}", daily_transfer_data[i][1])
            update_cell_value(state, historical_spreadsheet, historical_worksheet, f"C{row}", daily_transfer_data[i][2])
            update_cell_value(state, historical_spreadsheet, historical_worksheet, f"D{row}", daily_transfer_data[i][3])
            update_cell_value(state, historical_spreadsheet, historical_worksheet, f"E{row}", daily_transfer_data[i][4])
            update_cell_value(state, historical_spreadsheet, historical_worksheet, f"F{row}", daily_transfer_data[i][5])
    return


def clean_up_auto_sheet(state) -> None:
    auto_spreadsheet = state.get('daily_auto_spreadsheet_name')
    auto_worksheet = state.get('daily_auto_worksheet_name')
    auto_sheet_data = state.get(f"worksheet_{auto_spreadsheet}{auto_worksheet}_values")
    if len(auto_sheet_data) > 1:
        for i in range(1, len(auto_sheet_data)):
            update_cell_value(state, auto_spreadsheet, auto_worksheet, f"A{i+1}", "")
            update_cell_value(state, auto_spreadsheet, auto_worksheet, f"B{i+1}", "")
    return


def main(state=None):
    if state is None:
        state = State()

    state.info("Establishing spreadsheet and worksheet names")
    date_spreadsheet_name = state.get("date_spreadsheet")
    date_worksheet_name = state.get("date_worksheet")
    daily_manual_spreadsheet_name = state.get("daily_manual_spreadsheet_name")
    daily_manual_worksheet_name = state.get("daily_manual_worksheet_name")
    daily_auto_spreadsheet_name = state.get("daily_auto_spreadsheet_name")
    daily_auto_worksheet_name = state.get("daily_auto_worksheet_name")
    core_spreadsheet_name = state.get("core_spreadsheet_name")
    core_worksheet_name = state.get("core_worksheet_name")

    state.info("Opening food daily and core worksheets")
    open_google_worksheet(state, date_spreadsheet_name, date_worksheet_name)
    open_google_worksheet(state, daily_manual_spreadsheet_name, daily_manual_worksheet_name)
    open_google_worksheet(state, daily_auto_spreadsheet_name, daily_auto_worksheet_name)
    open_google_worksheet(state, core_spreadsheet_name, core_worksheet_name)

    state.info("Taking current date")
    get_current_date(state)

    state.info("Reading 'Auto' sheet")
    get_auto_sheet_values(state)
    state.info("Reading 'Manual' sheet")
    get_manual_sheet_values(state)
    state.info("Reading 'Historical Tracker' sheet")
    get_historical_sheet_values(state)

    state.info("Initialising transfer lists")
    assemble_daily_food_transfer_data(state)

    state.info("Sleeping for 101 seconds")
    time.sleep(101)
    state.info("transferring lists to historical tracker")
    transfer_daily_data_to_historical_sheet(state)

    state.info("Sleeping for 101 seconds")
    time.sleep(101)
    state.info("Blanking auto items")
    clean_up_auto_sheet(state)

    food_daily_manual_values = state.get(f"worksheet_{daily_manual_spreadsheet_name}{daily_manual_worksheet_name}_values")
    if len(food_daily_manual_values) > 2:
        state.info("Sleeping for 101 seconds")
        time.sleep(101)
        state.info("Blanking manual items")
        for i in range(1, len(food_daily_manual_values)):
            row = str(i+1)
            update_cell_value(state, "FoodDaily", "Manual", 'A%s' % row, "")
            update_cell_value(state, "FoodDaily", "Manual", 'B%s' % row, "")
            update_cell_value(state, "FoodDaily", "Manual", 'C%s' % row, "")
            update_cell_value(state, "FoodDaily", "Manual", 'D%s' % row, "")
            update_cell_value(state, "FoodDaily", "Manual", 'E%s' % row, "")
        state.info("finished")
    else:
        state.info("no manual items to blank")

    state.info("Finished running script")
    print("Done.")

#main()
