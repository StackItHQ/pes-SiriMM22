# google_sheets.py
import os
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]
SPREADSHEET_ID = "1zuiGcx_FpNom26Tkqd1MqAaj7OY8WtMB6L_4VY0FliA"
SHEET_RANGE = "Sheet1!A:E"

def get_service():
    creds = None
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
            creds = flow.run_local_server(port=0)
        with open("token.json", "w") as token:
            token.write(creds.to_json())
    return build("sheets", "v4", credentials=creds)

def read_data(service):
    try:
        sheet = service.spreadsheets()
        result = sheet.values().get(spreadsheetId=SPREADSHEET_ID, range=SHEET_RANGE).execute()
        values = result.get("values", [])
        return values
    except HttpError as err:
        print(f"An error occurred: {err}")
        return []

def create_data(service, new_values):
    try:
        sheet = service.spreadsheets()
        request = sheet.values().append(spreadsheetId=SPREADSHEET_ID, range=SHEET_RANGE, valueInputOption="USER_ENTERED", body={"values": new_values})
        response = request.execute()
        print(f"\nAppended {response.get('updates').get('updatedRows')} rows.")
    except HttpError as err:
        print(f"An error occurred: {err}")

def update_data(service, row_index, new_data):
    try:
        sheet = service.spreadsheets()
        range_name = f"Sheet1!A{row_index}:E{row_index}"
        request = sheet.values().update(spreadsheetId=SPREADSHEET_ID, range=range_name, valueInputOption="USER_ENTERED", body={"values": [new_data]})
        response = request.execute()
        print(f"\nUpdated row {row_index}.")
    except HttpError as err:
        print(f"An error occurred: {err}")

def delete_data(service, row_index):
    try:
        sheet = service.spreadsheets()
        range_name = f"Sheet1!A{row_index}:E{row_index}"
        request = sheet.values().clear(spreadsheetId=SPREADSHEET_ID, range=range_name).execute()
        print(f"\nCleared row {row_index}.")
    except HttpError as err:
        print(f"An error occurred: {err}")
