import os
from httplib2 import Http
from pprint import pprint

from django.core.management.base import BaseCommand, CommandError

from oauth2client import file, client, tools
from googleapiclient.discovery import build

SCOPES = 'https://www.googleapis.com/auth/spreadsheets.readonly'
FILE_ID = "12dM2qPbnE-RvHwWLrTOSN-lTkoYV9UyZex0eMvD_IEw"
SAMPLE_RANGE_NAME = 'Data!A2:E'

def get_questions():
    store = file.Storage('token.json')
    creds = store.get()
    pprint(creds)

    if not creds or creds.invalid:
        flow = client.flow_from_clientsecrets('credentials.json', SCOPES)
        creds = tools.run_flow(flow, store)
    service = build('sheets', 'v4', http=creds.authorize(Http()))

    sheet = service.spreadsheets()
    result = sheet.values().get(spreadsheetId=FILE_ID,
                                range=SAMPLE_RANGE_NAME).execute()
    values = result.get('values', [])

    if not values:
        print('No data found.')
    # else:
    #     for row in values:
    #         # Print columns A and E, which correspond to indices 0 and 4.
    #         print(row)
    return values