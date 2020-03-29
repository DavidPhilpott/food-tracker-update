import datetime
import os
import time
import gspread
import logging
from oauth2client.service_account import ServiceAccountCredentials

SCRIPT_NAME = "Food Daily Transfer"

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


def main():
    logger.info("Running %s..." %SCRIPT_NAME)

    runTime = str(datetime.datetime.now())
    logger.info("\nRunning%s...\nTime: %s\n" %(SCRIPT_NAME, runTime))

    logger.info("Assembling google auth path\n")
    authPath = assemble_absolute_path(GOOGLE_AUTH_FILENAME)
    logger.info("Requesting client from google using auth\n")
    sheets = request_google_sheet_client(credentials_path=authPath)
    logger.info("Opening food daily sheet\n")
    foodDaily = sheets.open_by_key('1rpHCHOHrdWr7LzL4lbc7xxXzuQ_UAIMl26MU2fbzyvU')
    logger.info("Opening food core sheet\n")
    foodCore = sheets.open_by_key('1QDq6rDSosVcLE-TekFcxGDLqvbn_leVa5vUo8uJMTSI')
    logger.info("Taking current date\n")
    currentDate = foodDaily.worksheet('Info').acell('C2').value
    logger.info("Opening 'Auto' sheet\n")
    foodDailyAuto = foodDaily.worksheet('Auto')
    logger.info("Opening 'Manual' sheet\n")
    foodDailyManual = foodDaily.worksheet('Manual')
    logger.info("Opening 'Historical Tracker\n")
    foodHistory = foodCore.worksheet('Historical Food Tracker')
    logger.info("Reading 'Auto' sheet\n")
    dfAuto = foodDailyAuto.get_all_values()
    logger.info("Reading 'Manual' sheet\n")
    dfManual = foodDailyManual.get_all_values()
    logger.info("Reading 'Historical Tracker' sheet\n")
    dfHistory = foodHistory.get_all_values()
    logger.info("Initialising transfer lists\n")
    transferDate = []
    transferItem = []
    transferQuantity = []
    transferCalorie = []
    transferProtein = []
    transferVeg = []
    logger.info("Appending auto items\n")
    if len(dfAuto) > 1:
        for i in range(1, len(dfAuto)):
            transferDate.append(currentDate)
            transferItem.append(dfAuto[i][0])
            transferQuantity.append(dfAuto[i][1])
            transferCalorie.append("")
            transferProtein.append("")
            transferVeg.append("")

    logger.info("Appending manual items\n")
    if len(dfManual) > 1:
        for i in range(1, len(dfManual)):
            transferDate.append(currentDate)
            transferItem.append(dfManual[i][0])
            transferQuantity.append(dfManual[i][1])
            transferCalorie.append(dfManual[i][2])
            transferProtein.append(dfManual[i][3])
            transferVeg.append(dfManual[i][4])
    startRow = len(dfHistory) + 1
    if len(transferDate) > 0:
        logger.info("Sleeping for 101 seconds\n")
        time.sleep(101)
        logger.info("transferring lists to historical tracker\n")
        for i in range(0, len(transferDate)):
            row = str(startRow + i)
            #foodHistory.update_acell('A%s' %row, transferDate[i])
            #foodHistory.update_acell('B%s' %row, transferItem[i])
            #foodHistory.update_acell('C%s' %row, transferQuantity[i])
            #foodHistory.update_acell('D%s' %row, transferCalorie[i])
            #foodHistory.update_acell('E%s' %row, transferProtein[i])
            #foodHistory.update_acell('F%s' %row, transferVeg[i])

        logger.info("finished transfering items\n")

    else:
        logger.info("Nothing to transfer\n")
    if len(dfAuto)>1:
        logger.info("Sleeping for 101 seconds\n")
        time.sleep(101)
        logger.info("Blanking auto items\n")
        for i in range(1, len(dfAuto)):
            row = str(i + 1)
            #foodDailyAuto.update_acell('A%s' %row, "")
            #foodDailyAuto.update_acell('B%s' %row, "")
        logger.info("finished\n")
    else:
        logger.info("No auto items to blank\n")
    if len(dfManual)>1:
        logger.info("Sleeping for 101 seconds\n")
        time.sleep(101)
        logger.info("Blanking manual items\n")
        for i in range(1, len(dfManual)):
            row = str(i+1)
            #foodDailyManual.update_acell('A%s' %row, "")
            #foodDailyManual.update_acell('B%s' %row, "")
            #foodDailyManual.update_acell('C%s' %row, "")
            #foodDailyManual.update_acell('D%s' %row, "")
            #foodDailyManual.update_acell('E%s' %row, "")
        logger.info("finished\n")
    else:
        logger.info("no manual items to blank\n")

    logger.info("Finished running script\n")
    print("Done.")

#main()
