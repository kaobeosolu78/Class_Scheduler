import time
import datetime
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/calendar']


def main(action, calendar, exam_dates):
    """Shows basic usage of the Google Calendar API.
    Prints the start and name of the next 10 events on the user's calendar.
    """
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

    service = build('calendar', 'v3', credentials=creds)
    if action == "clear":
        service.calendars().clear(calendarId='primary').execute()

    if action == "add":
        for exam in calendar:
            for chapter, data in list(exam.items()):
                for info in data: # add more descriptive names
                    service.events().quickAdd(
                        calendarId='primary',
                        text=f"{chapter}, page {info[1][0]} to pg. {info[1][1]}").execute()
                    time.sleep(1)

        for exam_num, date in enumerate(exam_dates):
            service.events().quickAdd(
                calendarId='primary',
                text=f"Exam {exam_num+1=} on {date}").execute()
            time.sleep(1)

# main("clear", "", "")