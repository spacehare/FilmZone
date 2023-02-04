from __future__ import print_function

import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from random import choice

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']

# The ID and range of a sample spreadsheet.
with open(r'configuration\google_sheet_id', 'r') as file:
    SPREADSHEET_ID: str = file.read()

# range is pre-filtered with active freaks on gSheet side
RANGE_NAME: str = 'META!J2:L'  # discord uid, human, indirect
ROLLS: int = 6
PATHS = {
    "token": "configuration/token.json",
    "credentials": "configuration/credentials.json",
}


def gsheet():  # -> Dict[str, List[int]] | None
    """Grab random picks from google sheet
    """
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists(PATHS['token']):
        creds = Credentials.from_authorized_user_file(PATHS['token'], SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                PATHS['credentials'], SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open(PATHS['token'], 'w') as token:
            token.write(creds.to_json())

    try:
        service = build('sheets', 'v4', credentials=creds)

        # Call the Sheets API
        sheet = service.spreadsheets()
        indirects = sheet.values().get(spreadsheetId=SPREADSHEET_ID,
                                       range=RANGE_NAME).execute()
        values = indirects.get('values', [])

        if not values:
            print('No data found.')
            return

        mane_list = []  # total film list. 'mane' bc 'The Mane Page'
        picks = []
        lucky_ones: list[int] = []

        # get data
        for uid, freak, indirect in values:
            films = sheet.values().get(spreadsheetId=SPREADSHEET_ID,
                                       range=indirect).execute().get('values', [])
            # https://stackoverflow.com/questions/952914/how-do-i-make-a-flat-list-out-of-a-list-of-lists
            # films = [item for sublist in films for item in sublist]  # flatten
            mane_list += [{'uid': uid, 'freak': freak, 'film': film[0], 'year': film[1] if len(film) > 1 else None}
                          for film in films]

        new_list = mane_list
        # roll
        for _ in range(ROLLS):
            pick = choice(new_list)
            print(pick)
            picks.append(pick)
            # remove picks (dupes) from new_list
            new_list = [ticket for ticket in new_list if ticket != pick]

        lucky_ones = list(set([pick['uid'] for pick in picks]))

        return {'lucky_ones': lucky_ones, 'picks': picks, 'mane_list': mane_list}

    except HttpError as err:
        print(err)


if __name__ == '__main__':
    gsheet()
