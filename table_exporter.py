import os.path
import json


from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
# The ID and range of a sample spreadsheet.
SAMPLE_SPREADSHEET_ID = None
with open('table_url.txt') as table_url:
        SAMPLE_SPREADSHEET_ID=table_url.read

creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
if os.path.exists('token.json'):
    creds = Credentials.from_authorized_user_file('token.json', SCOPES)
# If there are no (valid) credentials available, let the user log in.
if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())
    else:
        flow = InstalledAppFlow.from_client_secrets_file(
            'credentials.json', SCOPES)
        creds = flow.run_local_server(port=0)
    # Save the credentials for the next run
    with open('token.json', 'w') as token:
        token.write(creds.to_json())
service = build('sheets', 'v4', credentials=creds)

# Call the Sheets API
sheet = service.spreadsheets()
# columns_raw = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID,
#                                   range="A1:B3").execute()
# columns_raw = columns_raw.get('values', [])
# print(columns_raw)

# values = [
#            ['A', 'B'],
#             ['C', 'D']
#         ]
# body = {
#            'values': values
# }

# service.spreadsheets().values().update(
#             spreadsheetId=SAMPLE_SPREADSHEET_ID, range="A1:B2",
#             valueInputOption="USER_ENTERED", body=body).execute()

def update():
    all_tickets=None
    with open('db.json') as f:
        all_tickets=json.load(f)
    table_data = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID,
                                  range="A:F").execute()
    table_data = table_data.get('values', [])
    print(table_data)
    print(len(table_data))

def add_new(ticket_id,name,surname,patronymic,phone,email):
    table_data = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID,
                                  range="A:F").execute()
    table_data = table_data.get('values', [])
    row_to_insert=len(table_data)+1
    body={
        'values':[[ticket_id,name,surname,patronymic,phone,email]]
    }
    service.spreadsheets().values().update(
            spreadsheetId=SAMPLE_SPREADSHEET_ID, range="A{row_to_insert}:F{row_to_insert}".format(row_to_insert=row_to_insert),
            valueInputOption="USER_ENTERED", body=body).execute()

# add_new("JOPA","Василий","Пенисный","Дождь","88005553535;","poshel@nahui.ru")