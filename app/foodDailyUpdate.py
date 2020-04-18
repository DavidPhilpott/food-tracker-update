import time
from app.State import State
from app.Sessions.GoogleSheetConnection import GoogleSheetConnection
from app.Sessions.GoogleWorksheetSession import GoogleWorksheetSession
from app.Actions.OpenGoogleWorksheetSession import open_google_worksheet_session
from app.Actions.OpenGoogleSheetsConnection import open_google_spreadsheet_connection


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
        transfer_data.append([current_date, auto_data[i][0], auto_data[i][1], '', '', ''])
    for i in range(1, len(manual_data)):
        transfer_data.append([current_date, manual_data[i][0], manual_data[i][1], manual_data[i][2], manual_data[i][3], manual_data[i][4]])

    for i in range(1, len(transfer_data)):
        for j in range(1, len(transfer_data[0])):
            if transfer_data[i][j] == ' -':
                transfer_data[i][j] = ''

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


def clean_up_manual_sheet(state) -> None:
    manual_spreadsheet = state.get('daily_manual_spreadsheet_name')
    manual_worksheet = state.get('daily_manual_worksheet_name')
    manual_sheet_data = state.get(f"worksheet_{manual_spreadsheet}{manual_worksheet}_values")
    if len(manual_sheet_data) > 1:
        for i in range(1, len(manual_sheet_data)):
            update_cell_value(state, manual_spreadsheet, manual_worksheet, f"A{i+1}", "")
            update_cell_value(state, manual_spreadsheet, manual_worksheet, f"B{i+1}", "")
            update_cell_value(state, manual_spreadsheet, manual_worksheet, f"C{i+1}", "")
            update_cell_value(state, manual_spreadsheet, manual_worksheet, f"D{i+1}", "")
            update_cell_value(state, manual_spreadsheet, manual_worksheet, f"E{i+1}", "")
    return


def main():
    state = State()

    state.info(__name__, "Establishing spreadsheet and worksheet names...")
    date_spreadsheet_name = state.get("date_spreadsheet")
    date_worksheet_name = state.get("date_worksheet")
    daily_manual_spreadsheet_name = state.get("daily_manual_spreadsheet_name")
    daily_manual_worksheet_name = state.get("daily_manual_worksheet_name")
    daily_auto_spreadsheet_name = state.get("daily_auto_spreadsheet_name")
    daily_auto_worksheet_name = state.get("daily_auto_worksheet_name")
    core_spreadsheet_name = state.get("core_spreadsheet_name")
    core_worksheet_name = state.get("core_worksheet_name")

    open_google_spreadsheet_connection(state)
    open_google_worksheet_session(state, date_spreadsheet_name, date_worksheet_name)
    open_google_worksheet_session(state, daily_manual_spreadsheet_name, daily_manual_worksheet_name)
    open_google_worksheet_session(state, daily_auto_spreadsheet_name, daily_auto_worksheet_name)
    open_google_worksheet_session(state, core_spreadsheet_name, core_worksheet_name)

    state.info(__name__, "Opening food daily and core worksheets...")
    open_google_worksheet(state, date_spreadsheet_name, date_worksheet_name)
    open_google_worksheet(state, daily_manual_spreadsheet_name, daily_manual_worksheet_name)
    open_google_worksheet(state, daily_auto_spreadsheet_name, daily_auto_worksheet_name)
    open_google_worksheet(state, core_spreadsheet_name, core_worksheet_name)

    state.info(__name__, "Taking current date...")
    get_current_date(state)

    state.info(__name__, "Reading 'Auto' sheet...")
    get_auto_sheet_values(state)
    state.info(__name__, "Reading 'Manual' sheet...")
    get_manual_sheet_values(state)
    state.info(__name__, "Reading 'Historical Tracker' sheet...")
    get_historical_sheet_values(state)

    state.info(__name__, "Initialising transfer lists...")
    assemble_daily_food_transfer_data(state)

    state.info(__name__, "Sleeping for 60 seconds...")
    time.sleep(60)
    state.info(__name__, "transferring lists to historical tracker...")
    transfer_daily_data_to_historical_sheet(state)

    state.info(__name__, "Sleeping for 60 seconds...")
    time.sleep(60)
    state.info(__name__, "Blanking auto items...")
    clean_up_auto_sheet(state)

    state.info(__name__, "Blanking manual items...")
    clean_up_manual_sheet(state)

    state.info(__name__, "Finished running script...")
    return


def lambda_handler(event, context):
    main()
    return
