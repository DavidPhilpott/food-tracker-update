import datetime
import os
import time
import gspread
import logging
from oauth2client.service_account import ServiceAccountCredentials

GOOGLE_AUTH_FILENAME = r'pyScripts/GoogleAuth.json'

logger = logging.getLogger(__name__)
logger.setLevel('DEBUG')


def assemble_absolute_path(file_name):
    absolute_path = os.path.join(os.path.expanduser('~'), file_name)
    return absolute_path


def request_google_sheet_client(credentials_path):
    service_scope = ['https://spreadsheets.google.com/feeds',
                     'https://www.googleapis.com/auth/drive']
    
    credentials = ServiceAccountCredentials.from_json_keyfile_name(credentials_path, service_scope)
    sheets_client = gspread.authorize(credentials)
    return sheets_client


def open_google_sheet(google_client, sheet_key):
    worksheet = google_client.open_by_key(sheet_key)
    return worksheet


def main():
    logger.info("Assembling google auth path\n")
    auth_path = assemble_absolute_path(GOOGLE_AUTH_FILENAME)
    logger.info("Requesting client from google using auth\n")
    sheets = request_google_sheet_client(credentials_path=auth_path)
    logger.info("Opening food daily sheet\n")
    food_daily = open_google_sheet(google_client=sheets, sheet_key='1rpHCHOHrdWr7LzL4lbc7xxXzuQ_UAIMl26MU2fbzyvU')
    logger.info("Opening food core sheet\n")
    food_core = open_google_sheet(google_client=sheets, sheet_key='1QDq6rDSosVcLE-TekFcxGDLqvbn_leVa5vUo8uJMTSI')
    logger.info("Taking current date\n")
    current_date = food_daily.worksheet('Info').acell('C2').value
    logger.info("Opening 'Auto' sheet\n")
    food_daily_auto = food_daily.worksheet('Auto')
    logger.info("Opening 'Manual' sheet\n")
    food_daily_manual = food_daily.worksheet('Manual')
    logger.info("Opening 'Historical Tracker\n")
    food_history = food_core.worksheet('Historical Food Tracker')
    logger.info("Reading 'Auto' sheet\n")
    df_auto_daily = food_daily_auto.get_all_values()
    logger.info("Reading 'Manual' sheet\n")
    df_manual_daily = food_daily_manual.get_all_values()
    logger.info("Reading 'Historical Tracker' sheet\n")
    df_food_history = food_history.get_all_values()
    logger.info("Initialising transfer lists\n")
    transfer_date = []
    transfer_item = []
    transfer_quantity = []
    transfer_calorie = []
    transfer_protein = []
    transfer_veg = []
    logger.info("Appending auto items\n")
    if len(df_auto_daily) > 1:
        for i in range(1, len(df_auto_daily)):
            transfer_date.append(current_date)
            transfer_item.append(df_auto_daily[i][0])
            transfer_quantity.append(df_auto_daily[i][1])
            transfer_calorie.append("")
            transfer_protein.append("")
            transfer_veg.append("")

    logger.info("Appending manual items\n")
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
        logger.info("Sleeping for 101 seconds\n")
        time.sleep(101)
        logger.info("transferring lists to historical tracker\n")
        for i in range(0, len(transfer_date)):
            row = str(start_row + i)
            #food_history.update_acell('A%s' %row, transfer_date[i])
            #food_history.update_acell('B%s' %row, transfer_item[i])
            #food_history.update_acell('C%s' %row, transfer_quantity[i])
            #food_history.update_acell('D%s' %row, transfer_calorie[i])
            #food_history.update_acell('E%s' %row, transfer_protein[i])
            #food_history.update_acell('F%s' %row, transfer_veg[i])

        logger.info("finished transfering items\n")

    else:
        logger.info("Nothing to transfer\n")
    if len(df_auto_daily)>1:
        logger.info("Sleeping for 101 seconds\n")
        time.sleep(101)
        logger.info("Blanking auto items\n")
        for i in range(1, len(df_auto_daily)):
            row = str(i + 1)
            #food_daily_auto.update_acell('A%s' %row, "")
            #food_daily_auto.update_acell('B%s' %row, "")
        logger.info("finished\n")
    else:
        logger.info("No auto items to blank\n")
    if len(df_manual_daily)>1:
        logger.info("Sleeping for 101 seconds\n")
        time.sleep(101)
        logger.info("Blanking manual items\n")
        for i in range(1, len(df_manual_daily)):
            row = str(i+1)
            #food_daily_manual.update_acell('A%s' %row, "")
            #food_daily_manual.update_acell('B%s' %row, "")
            #food_daily_manual.update_acell('C%s' %row, "")
            #food_daily_manual.update_acell('D%s' %row, "")
            #food_daily_manual.update_acell('E%s' %row, "")
        logger.info("finished\n")
    else:
        logger.info("no manual items to blank\n")

    logger.info("Finished running script\n")
    print("Done.")

#main()
