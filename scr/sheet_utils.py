import gspread
from oauth2client.service_account import ServiceAccountCredentials
from openpyxl.utils.cell import get_column_letter
import pandas as pd
import numpy as np

def get_worksheet_details(worksheet):
    existing_data=worksheet.get_all_values()
    LAST_LINE=len(existing_data)
    return LAST_LINE
    
def authorize_gspread(TOKEN_PATH):
    ## must store credentials 
    SCOPES = ["https://spreadsheets.google.com/feeds",'https://www.googleapis.com/auth/spreadsheets',
     "https://www.googleapis.com/auth/drive.file","https://www.googleapis.com/auth/drive"]
    if TOKEN_PATH.exists():
        creds=ServiceAccountCredentials.from_json_keyfile_name(TOKEN_PATH, SCOPES)
        return gspread.authorize(creds)
    else:
        print("could not authorize")

def update_sheets(
    sheet_filename,
    work_sheet_name,
    TITLE_ROW,
    updated_data,
    TOKEN_PATH
                 ):
    client=authorize_gspread(TOKEN_PATH)
    spreadsheet=client.open(sheet_filename)
    worksheet=spreadsheet.worksheet(work_sheet_name)
    space=1
    
    if isinstance(updated_data,pd.DataFrame):
        print("true dat")
        columns=updated_data.columns
        updated_data=updated_data.astype(str)
        data=updated_data.values.tolist()

    columns_number=len(data[0])
    LAST_LINE=get_worksheet_details(worksheet)  
    range_name=f'A{LAST_LINE+1+space}:{get_column_letter(columns_number)}{(LAST_LINE+1+space)+len(data)}'
    print(range_name)
    worksheet.update(range_name,data)
    
def get_sheets(
    sheet_filename,
    work_sheet_name,
    TITLE_ROW,
    TOKEN_PATH
):
    
    client=authorize_gspread(TOKEN_PATH)
    spreadsheet=client.open(sheet_filename)
    worksheet=spreadsheet.worksheet(work_sheet_name)
    all_data=worksheet.get_all_values()
    titles=all_data[TITLE_ROW-1]
    data=all_data[TITLE_ROW:]
    return pd.DataFrame(data,columns=titles)