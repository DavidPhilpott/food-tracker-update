import time
from app.State import State
from app.Sessions.GoogleSheetConnection import GoogleSheetConnection
from app.Sessions.GoogleWorksheetSession import GoogleWorksheetSession
from app.Actions.OpenGoogleWorksheetSession import open_google_worksheet_session
from app.Actions.OpenGoogleSheetsConnection import open_google_spreadsheet_connection
from app.Domain_Actions.GetCurrentDate import get_current_date
from app.Domain_Actions.GetAutoSheetValues import get_auto_sheet_values
from app.Domain_Actions.GetManualSheetValues import get_manual_sheet_values
from app.Domain_Actions.GetHistoricalSheetValues import get_historical_sheet_values
from app.Domain_Actions.AssembleDailyFoodTransferData import assemble_daily_food_transfer_data
from app.Domain_Actions.TransferDailyDataToHistoricalSheet import transfer_daily_data_to_historical_sheet
from app.Domain_Actions.CleanUpAutoSheet import clean_up_auto_sheet
from app.Domain_Actions.CleanUpManualSheet import clean_up_manual_sheet


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


def main():
    state = State()
    state.info(__name__, "State set - starting script.")

    open_google_spreadsheet_connection(state)
    open_google_worksheet_session(state, state.get("date_spreadsheet"), state.get("date_worksheet"), 'date_worksheet')
    open_google_worksheet_session(state, state.get("daily_manual_spreadsheet_name"), state.get("daily_manual_worksheet_name"), 'daily_manual_worksheet')
    open_google_worksheet_session(state, state.get("daily_auto_spreadsheet_name"), state.get("daily_auto_worksheet_name"), 'daily_auto_worksheet')
    open_google_worksheet_session(state, state.get("core_spreadsheet_name"), state.get("core_worksheet_name"), 'historical_core_worksheet')

    get_current_date(state)
    get_auto_sheet_values(state)
    get_manual_sheet_values(state)
    get_historical_sheet_values(state)

    assemble_daily_food_transfer_data(state)

    state.info(__name__, "Sleeping for 60 seconds...")
    time.sleep(60)

    transfer_daily_data_to_historical_sheet(state)

    state.info(__name__, "Sleeping for 60 seconds...")
    time.sleep(60)

    state.info(__name__, "Blanking auto items...")
    clean_up_auto_sheet(state)

    state.info(__name__, "Blanking manual items...")
    clean_up_manual_sheet(state)

    state.info(__name__, "Finished running script.")
    return


def lambda_handler(event, context):
    main()
    return
