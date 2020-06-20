#!/usr/bin/env python3

import pickle
import os.path

from pprint import pprint

from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

_COLUMN_HEADERS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'

_SPREADSHEET_ID = '1Rz9jxXhuT_qwkujlU35llzlcLyxj51fvlA9re4Wx22g'
_RANGE_NAME = 'Source Data!A:D'


def _Authorize():
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
            with open('token.pickle', 'rb') as token:
                creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    return creds


def ColumnRange(sheet_name, rows):
    if len(rows) == 0:
        raise ValueError('No rows')
    if len(rows[0]) > len(_COLUMN_HEADERS):
        raise ValueError('Too many columns: %d' % len(rows[0]))
    range = "'%s'!A:%s" % (sheet_name, _COLUMN_HEADERS[len(rows[0]) - 1])
    return range


def ReadSheet():
    creds = _Authorize()
    service = build('sheets', 'v4', credentials=creds)

    result = service.spreadsheets().values().get(
        spreadsheetId=_SPREADSHEET_ID,
        range=_RANGE_NAME)
    response = result.execute()
    pprint(response)


def WriteSheet(sheet_id, range, values):
    creds = _Authorize()
    service = build('sheets', 'v4', credentials=creds)

    body = {
        'range': range,
        'values': values,
    }
    request = service.spreadsheets().values().update(
        spreadsheetId=sheet_id,
        range=range,
        valueInputOption='USER_ENTERED',
        body=body)
    response = request.execute()
    pprint(response)
