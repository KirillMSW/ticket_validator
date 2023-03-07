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
        SAMPLE_SPREADSHEET_ID=table_url.read()

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

ROW_NUM=6
def update_status(ticket_id,status):
    table_data = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID,
                                  range="A:A").execute()
    table_data = table_data.get('values', [])
    row_to_update = None
    for i in range(len(table_data)):
        if ticket_id in table_data[i]:
            row_to_update=i

    if row_to_update!=None:
        row_to_update+=1
        body={
        'values':[[status]]
        }
        service.spreadsheets().values().update(
                spreadsheetId=SAMPLE_SPREADSHEET_ID, range="B{row_to_update}".format(row_to_update=row_to_update),
                valueInputOption="USER_ENTERED", body=body).execute()


def void_table(ticket_id):
    table_data = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID,
                                  range="A").execute()
    table_data = table_data.get('values', [])
    row_to_delete = None
    for i in range(len(table_data)):
        if ticket_id in table_data[i]:
            row_to_delete=i

    if row_to_delete!=None:
        row_to_delete+=1
        body={
        'values':[["АННУЛИРОВАН"]]
        }
        service.spreadsheets().values().update(
                spreadsheetId=SAMPLE_SPREADSHEET_ID, range="B{row_to_delete}".format(row_to_delete=row_to_delete),
                valueInputOption="USER_ENTERED", body=body).execute()

    # format_values=[]
    # if row_to_delete!=None:
    #     for i in range(ROW_NUM):
    #         format_values.append({
    #                                 "userEnteredFormat": {
    #                                     "textFormat":{

    #                                     "foregroundColorStyle": {
    #                                         "rgbColor": {
    #                                         "red": 1,
    #                                         "green": 0,
    #                                         "blue": 0,
    #                                         "alpha": 1
    #                                 }}}}})
    #     requests =[]

    #     requests.append({
    #                 "updateCells": {
    #                 "rows": [
    #                     {
    #                         "values": format_values
    #                     }
    #                 ],
    #                 "fields": 'userEnteredFormat.textFormat.foregroundColorStyle',
    #                 "start": {
    #                     "sheetId": 0,
    #                     "rowIndex":row_to_delete,
    #                     "columnIndex": 0
    #                 }}})
    #     final_body={
    #         "requests":requests
    #     }
    #     service.spreadsheets().batchUpdate(
    #             spreadsheetId=SAMPLE_SPREADSHEET_ID, body=final_body).execute()

def add_new(ticket_id,surname,name,patronymic,phone,email):
    table_data = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID,
                                  range="A:A").execute()
    table_data = table_data.get('values', [])
    row_to_insert=len(table_data)+1
    body={
        'values':[[ticket_id,"АКТИВЕН",surname,name,patronymic,phone,email]]
    }
    service.spreadsheets().values().update(
            spreadsheetId=SAMPLE_SPREADSHEET_ID, range="A{row_to_insert}:G{row_to_insert}".format(row_to_insert=row_to_insert),
            valueInputOption="USER_ENTERED", body=body).execute()

# add_new("JOPA","Василий","Пенисный","Дождь","88005553535;","poshel@nahui.ru")


