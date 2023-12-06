from __future__ import print_function

import re

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from oauth2client.service_account import ServiceAccountCredentials
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
    "service": "configuration/service.json",
}
regex_grab_cell = r'(.+)!(\w)(\d+)[:]'


def gsheet():
    """Grab random picks from google sheet
    """
    creds = ServiceAccountCredentials.from_json_keyfile_name(
        PATHS['service'], SCOPES)

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
            # cell_int: int = raw_cell_coord.group(3)
            def cell_coord(index: int):
                raw_cell_coord = re.search(regex_grab_cell, indirect)
                sheet: str = raw_cell_coord.group(1)
                letter: str = raw_cell_coord.group(2)
                number: int = int(raw_cell_coord.group(3)) + index
                return f"{sheet}!{letter}{number}"

            films = sheet.values().get(spreadsheetId=SPREADSHEET_ID,
                                       range=indirect).execute().get('values', [])

            # if someone has a blank movie, remove it
            films = [film for film in films if film]

            mane_list += [{'cell': cell_coord(idx), 'uid': uid, 'freak': freak, 'film': film[0], 'year': film[1] if len(film) > 1 else None}
                          for idx, film in enumerate(films)]

        new_list = mane_list
        # roll
        for _ in range(ROLLS):
            pick = choice(new_list)
            print(pick)
            picks.append(pick)
            # remove picks (dupes) from new_list
            new_list = [
                ticket for ticket in new_list if ticket['film'].lower() != pick['film'].lower()]

        lucky_ones = list(set([pick['uid'] for pick in picks]))

        return {'lucky_ones': lucky_ones, 'picks': picks, 'mane_list': mane_list}

    except HttpError as err:
        print(err)


if __name__ == '__main__':
    gsheet()
