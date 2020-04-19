import time
from app.State import State
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


def main():
    state = State()
    state.info(__name__, "Starting script.")

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

    clean_up_auto_sheet(state)
    clean_up_manual_sheet(state)
    state.info(__name__, "Finished running script.")
    return


def lambda_handler(event, context):
    main()
    return
