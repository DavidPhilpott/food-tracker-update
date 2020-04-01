import os
import time
import gspread
import logging
from oauth2client.service_account import ServiceAccountCredentials
from State import State
from GoogleSheetConnection import GoogleSheetConnection

GOOGLE_AUTH_FILENAME = r'pyScripts/GoogleAuth.json'


def open_google_worksheet(google_client, sheet_key):
    worksheet = google_client.open_by_key(sheet_key)
    return worksheet


def get_all_sheet_values(google_sheet):
    df_result = google_sheet.get_all_values()
    return df_result


def get_cell_value(google_sheet, cell_index):
    cell_value = google_sheet.acell(cell_index).value
    return cell_value


def update_cell_value(google_sheet, cell_index, value):
    google_sheet.update_acell(cell_index, value)
    return


def main(state=None):
    if state is None:
        state = State()
    state.info("Requesting client from google using auth")
    sheets = GoogleSheetConnection(state).connection
    state.info("Opening food daily and core worksheets")
    food_daily = open_google_worksheet(google_client=sheets, sheet_key='1rpHCHOHrdWr7LzL4lbc7xxXzuQ_UAIMl26MU2fbzyvU')
    food_core = open_google_worksheet(google_client=sheets, sheet_key='1QDq6rDSosVcLE-TekFcxGDLqvbn_leVa5vUo8uJMTSI')

    state.info("Opening specific sheets")
    food_daily_info = food_daily.worksheet('Info')
    food_daily_auto = food_daily.worksheet('Auto')
    food_daily_manual = food_daily.worksheet('Manual')
    food_history = food_core.worksheet('Historical Food Tracker')

    state.info("Taking current date")
    current_date = get_cell_value(google_sheet=food_daily_info, cell_index='C2')

    state.info("Reading 'Auto' sheet")
    df_auto_daily = get_all_sheet_values(food_daily_auto)

    state.info("Reading 'Manual' sheet")
    df_manual_daily = get_all_sheet_values(food_daily_manual)

    state.info("Reading 'Historical Tracker' sheet")
    df_food_history = get_all_sheet_values(food_history)

    state.info("Initialising transfer lists")
    transfer_date = []
    transfer_item = []
    transfer_quantity = []
    transfer_calorie = []
    transfer_protein = []
    transfer_veg = []
    state.info("Appending auto items")
    if len(df_auto_daily) > 1:
        for i in range(1, len(df_auto_daily)):
            transfer_date.append(current_date)
            transfer_item.append(df_auto_daily[i][0])
            transfer_quantity.append(df_auto_daily[i][1])
            transfer_calorie.append("")
            transfer_protein.append("")
            transfer_veg.append("")

    state.info("Appending manual items")
    if len(df_manual_daily) > 1:
        for i in range(1, len(df_manual_daily)):
            transfer_date.append(current_date)
            transfer_item.append(df_manual_daily[i][0])
            transfer_quantity.append(df_manual_daily[i][1])
            transfer_calorie.append(df_manual_daily[i][2])
            transfer_protein.append(df_manual_daily[i][3])
            transfer_veg.append(df_manual_daily[i][4])
    start_row = len(df_food_history) + 1
    if len(transfer_date) > 0:
        state.info("Sleeping for 101 seconds")
        time.sleep(101)
        state.info("transferring lists to historical tracker")
        for i in range(0, len(transfer_date)):
            row = str(start_row + i)
            update_cell_value(google_sheet=food_history, cell_index='A%s' % row, value=transfer_date[i])
            update_cell_value(google_sheet=food_history, cell_index='B%s' % row, value=transfer_item[i])
            update_cell_value(google_sheet=food_history, cell_index='C%s' % row, value=transfer_quantity[i])
            update_cell_value(google_sheet=food_history, cell_index='D%s' % row, value=transfer_calorie[i])
            update_cell_value(google_sheet=food_history, cell_index='E%s' % row, value=transfer_protein[i])
            update_cell_value(google_sheet=food_history, cell_index='F%s' % row, value=transfer_veg[i])
        state.info("finished transferring items")

    else:
        state.info("Nothing to transfer")
    if len(df_auto_daily) > 1:
        state.info("Sleeping for 101 seconds")
        time.sleep(101)
        state.info("Blanking auto items")
        for i in range(1, len(df_auto_daily)):
            row = str(i + 1)
            update_cell_value(google_sheet=food_daily_auto, cell_index='A%s' % row, value="")
            update_cell_value(google_sheet=food_daily_auto, cell_index='B%s' % row, value="")
        state.info("finished")
    else:
        state.info("No auto items to blank")
    if len(df_manual_daily) > 1:
        state.info("Sleeping for 101 seconds")
        time.sleep(101)
        state.info("Blanking manual items")
        for i in range(1, len(df_manual_daily)):
            row = str(i+1)
            update_cell_value(google_sheet=food_daily_manual, cell_index='A%s' % row, value="")
            update_cell_value(google_sheet=food_daily_manual, cell_index='B%s' % row, value="")
            update_cell_value(google_sheet=food_daily_manual, cell_index='C%s' % row, value="")
            update_cell_value(google_sheet=food_daily_manual, cell_index='D%s' % row, value="")
            update_cell_value(google_sheet=food_daily_manual, cell_index='E%s' % row, value="")
        state.info("finished")
    else:
        state.info("no manual items to blank")

    state.info("Finished running script")
    print("Done.")

#main()
