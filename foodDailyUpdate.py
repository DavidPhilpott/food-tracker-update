import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd

import datetime

import gspread_dataframe as gsdf

import time

import os

SCRIPT_NAME = "Food Daily Transfer"

GOOGLE_AUTH_FILENAME = r'projects/food-tracker-update/GoogleAuth.json'
LOG_FILENAME = r'projects/food-tracker-update/FoodDailyTransferLog.txt'

def assembleAbsolutePath(fileName):
    
    absolutePath = os.path.join(os.path.expanduser('~'), fileName)
    
    return absolutePath

def requestGoogleSheetClient(credentialsPath):
    
    scope = ['https://spreadsheets.google.com/feeds',
             'https://www.googleapis.com/auth/drive']
    
    credentials = ServiceAccountCredentials.from_json_keyfile_name(credentialsPath, scope)
    sheetsClient = gspread.authorize(credentials)
    
    return sheetsClient   
    
def main():

    print("Running %s..." %SCRIPT_NAME, end = '')
    
    logPath = assembleAbsolutePath(LOG_FILENAME)
    
    with open(logPath, 'a') as logFile:
        
        runTime = str(datetime.datetime.now())
        logFile.write("\nRunning%s...\nTime: %s\n" %(SCRIPT_NAME, runTime))
        
        logFile.write("Assembling google auth path\n")
        authPath = assembleAbsolutePath(GOOGLE_AUTH_FILENAME)

        logFile.write("Requesting client from google using auth\n")
        sheets = requestGoogleSheetClient(credentialsPath=authPath)

        logFile.write("Opening food daily sheet\n")
        foodDaily = sheets.open_by_key('1rpHCHOHrdWr7LzL4lbc7xxXzuQ_UAIMl26MU2fbzyvU')
        logFile.write("Opening food core sheet\n")
        foodCore = sheets.open_by_key('1QDq6rDSosVcLE-TekFcxGDLqvbn_leVa5vUo8uJMTSI')

        logFile.write("Taking current date\n")
        currentDate = foodDaily.worksheet('Info').acell('C2').value

        logFile.write("Opening 'Auto' sheet\n")
        foodDailyAuto = foodDaily.worksheet('Auto')
        logFile.write("Opening 'Manual' sheet\n")
        foodDailyManual = foodDaily.worksheet('Manual')
        logFile.write("Opening 'Historical Tracker\n")
        foodHistory = foodCore.worksheet('Historical Food Tracker')

        logFile.write("Reading 'Auto' sheet\n")
        dfAuto = foodDailyAuto.get_all_values()
        logFile.write("Reading 'Manual' sheet\n")
        dfManual = foodDailyManual.get_all_values()
        logFile.write("Reading 'Historical Tracker' sheet\n")
        dfHistory = foodHistory.get_all_values()

        logFile.write("Initialising transfer lists\n")
        transferDate = []
        transferItem = []
        transferQuantity = []
        transferCalorie = []
        transferProtein = []
        transferVeg = []

        logFile.write("Appending auto items\n")
        if len(dfAuto) > 1:
            for i in range(1, len(dfAuto)):
                transferDate.append(currentDate)
                transferItem.append(dfAuto[i][0])
                transferQuantity.append(dfAuto[i][1])
                transferCalorie.append("")
                transferProtein.append("")
                transferVeg.append("")

                
        logFile.write("Appending manual items\n")
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
            logFile.write("Sleeping for 101 seconds\n")
            time.sleep(101)
            logFile.write("transferring lists to historical tracker\n")
            for i in range(0, len(transferDate)):
                row = str(startRow + i)

                foodHistory.update_acell('A%s' %row, transferDate[i])
                foodHistory.update_acell('B%s' %row, transferItem[i])
                foodHistory.update_acell('C%s' %row, transferQuantity[i])
                foodHistory.update_acell('D%s' %row, transferCalorie[i])
                foodHistory.update_acell('E%s' %row, transferProtein[i])
                foodHistory.update_acell('F%s' %row, transferVeg[i])
                
            logFile.write("finished transfering items\n")
            
        else:
            logFile.write("Nothing to transfer\n")

        if len(dfAuto)>1:
            logFile.write("Sleeping for 101 seconds\n")
            time.sleep(101)
            logFile.write("Blanking auto items\n")
            for i in range(1, len(dfAuto)):
                row = str(i + 1)
                foodDailyAuto.update_acell('A%s' %row, "")
                foodDailyAuto.update_acell('B%s' %row, "")
            logFile.write("finished\n")
        else:
            logFile.write("No auto items to blank\n")

        if len(dfManual)>1:
            logFile.write("Sleeping for 101 seconds\n")
            time.sleep(101)
            logFile.write("Blanking manual items\n")
            for i in range(1, len(dfManual)):
                row = str(i+1)
                foodDailyManual.update_acell('A%s' %row, "")
                foodDailyManual.update_acell('B%s' %row, "")
                foodDailyManual.update_acell('C%s' %row, "")
                foodDailyManual.update_acell('D%s' %row, "")
                foodDailyManual.update_acell('E%s' %row, "")
            logFile.write("finished\n")
        else:
            logFile.write("no manual items to blank\n")
        
        logFile.write("Finished running script\n")
        
    logFile.close()
    print("Done.")

#main()
