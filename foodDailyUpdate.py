import time
from State import State
from GoogleSheetConnection import GoogleSheetConnection
from GoogleWorksheetSession import GoogleWorksheetSession


def update_cell_value(state, spreadsheet_name, worksheet_name, cell_index, value):
    worksheet = state.get(f"worksheet_{spreadsheet_name}{worksheet_name}")
    worksheet.update_cell_value(cell_index, value)
    return


def open_google_worksheet(state, spreadsheet_name: str, worksheet_name: str):
    worksheet = GoogleWorksheetSession(state, GoogleSheetConnection(state), spreadsheet_name, worksheet_name)
    state.set({f"worksheet_{spreadsheet_name}{worksheet_name}": worksheet})
    return


def get_sheet_cell_value(state, spreadsheet_name, worksheet_name, index):
    worksheet = state.get(f"worksheet_{spreadsheet_name}{worksheet_name}")
    return worksheet.get_cell_value(index)


def get_all_sheet_values(state, spreadsheet_name, worksheet_name):
    worksheet = state.get(f"worksheet_{spreadsheet_name}{worksheet_name}")
    return worksheet.get_all_sheet_values()


def main(state=None):
    if state is None:
        state = State()

    state.info("Opening food daily and core worksheets")
    open_google_worksheet(state, "FoodDaily", "Info")
    open_google_worksheet(state, "FoodDaily", "Auto")
    open_google_worksheet(state, "FoodDaily", "Manual")
    open_google_worksheet(state, "FoodCore", "Historical Food Tracker")

    state.info("Taking current date")
    current_date = get_sheet_cell_value(state, "FoodDaily", "Info", "C2")

    state.info("Reading 'Auto' sheet")
    food_daily_auto_values = get_all_sheet_values(state, "FoodDaily", "Auto")
    state.info("Reading 'Manual' sheet")
    food_daily_manual_values = get_all_sheet_values(state, "FoodDaily", "Manual")
    state.info("Reading 'Historical Tracker' sheet")
    food_history_values = get_all_sheet_values(state, "FoodCore", "Historical Food Tracker")

    state.info("Initialising transfer lists")
    transfer_date = []
    transfer_item = []
    transfer_quantity = []
    transfer_calorie = []
    transfer_protein = []
    transfer_veg = []
    state.info("Appending auto items")
    if len(food_daily_auto_values) > 1:
        for i in range(1, len(food_daily_auto_values)):
            transfer_date.append(current_date)
            transfer_item.append(food_daily_auto_values[i][0])
            transfer_quantity.append(food_daily_auto_values[i][1])
            transfer_calorie.append("")
            transfer_protein.append("")
            transfer_veg.append("")

    state.info("Appending manual items")
    if len(food_daily_manual_values) > 1:
        for i in range(1, len(food_daily_manual_values)):
            transfer_date.append(current_date)
            transfer_item.append(food_daily_manual_values[i][0])
            transfer_quantity.append(food_daily_manual_values[i][1])
            transfer_calorie.append(food_daily_manual_values[i][2])
            transfer_protein.append(food_daily_manual_values[i][3])
            transfer_veg.append(food_daily_manual_values[i][4])
    start_row = len(food_history_values) + 1
    if len(transfer_date) > 0:
        state.info("Sleeping for 101 seconds")
        time.sleep(101)
        state.info("transferring lists to historical tracker")
        for i in range(0, len(transfer_date)):
            row = str(start_row + i)
            update_cell_value(state, "FoodCore", "Historical Food Tracker", 'A%s' % row, transfer_date[i])
            update_cell_value(state, "FoodCore", "Historical Food Tracker", 'B%s' % row, transfer_item[i])
            update_cell_value(state, "FoodCore", "Historical Food Tracker", 'C%s' % row, transfer_quantity[i])
            update_cell_value(state, "FoodCore", "Historical Food Tracker", 'D%s' % row, transfer_calorie[i])
            update_cell_value(state, "FoodCore", "Historical Food Tracker", 'E%s' % row, transfer_protein[i])
            update_cell_value(state, "FoodCore", "Historical Food Tracker", 'F%s' % row, transfer_veg[i])
        state.info("finished transferring items")

    else:
        state.info("Nothing to transfer")
    if len(food_daily_auto_values) > 1:
        state.info("Sleeping for 101 seconds")
        time.sleep(101)
        state.info("Blanking auto items")
        for i in range(1, len(food_daily_auto_values)):
            row = str(i + 1)
            update_cell_value(state, "FoodDaily", "Auto", 'A%s' % row, "")
            update_cell_value(state, "FoodDaily", "Auto", 'B%s' % row, "")
        state.info("finished")
    else:
        state.info("No auto items to blank")
    if len(food_daily_manual_values) > 1:
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
