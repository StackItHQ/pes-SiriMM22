import os
import time
import mysql.connector
from googleapiclient.discovery import build
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from database import get_db_connection, create_in_db
from googleapiclient.errors import HttpError

SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]
SPREADSHEET_ID = "1zuiGcx_FpNom26Tkqd1MqAaj7OY8WtMB6L_4VY0FliA"
RANGE_NAME = "Sheet1!A:D"

def get_google_sheets_service():
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

def fetch_sheet_data(service):
    try:
        result = service.spreadsheets().values().get(
            spreadsheetId=SPREADSHEET_ID, range=RANGE_NAME
        ).execute()
        values = result.get('values', [])

        return values[1:] if len(values) > 1 else []
    except HttpError as err:
        print(f"Google Sheets API error: {err}")
        return []

def sync():
    sheets_service = get_google_sheets_service()
    db_connection = get_db_connection()
    if db_connection:
        sheet_data = fetch_sheet_data(sheets_service)
        
        if sheet_data:
            create_in_db(db_connection, sheet_data)

        db_connection.close()

if __name__ == "__main__":
    while True:
        sync()
        time.sleep(30)  
