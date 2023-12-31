import os.path
from datetime import datetime


from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/calendar"]


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
    return build("calendar", "v3", credentials=creds)


def get_calendars(service):
    calendars = service.calendarList().list().execute()
    return calendars


def get_school_calendar(service=get_service()):
    calendars = get_calendars(service)
    return [
        calendar for calendar in calendars["items"] if calendar["summary"] == "school"
    ][0]


def get_all_events_from_google_calendar(service, calendarId, start_date, end_date):
    events_result = (
        service.events()
        .list(
            calendarId=calendarId,
            timeMin=start_date.strftime("%Y-%m-%dT%H:%M:%SZ"),
            timeMax=end_date.strftime("%Y-%m-%dT%H:%M:%SZ"),
            singleEvents=True,
            orderBy="startTime",
        )
        .execute()
    )
    events = events_result.get("items", [])
    return events


def convert_to_datetime(date_string):
    return datetime.strptime(date_string, "%Y-%m-%dT%H:%M:%S%z")


def check_if_event_exists(service, calendarId, name, room, details, start, end):
    # converts the following date format into a datetime object
    # 2024-01-18T12:20:00+00:00

    end = convert_to_datetime(end)
    start = convert_to_datetime(start)

    events = get_all_events_from_google_calendar(service, calendarId, start, end)
    if events == []:
        return False
    return events


def get_colorId(name):
    return ("8"
        if name == "Supervised Study"
        else "7"
        if name == "Physics"
        else "6"
        if name == "Mathematic"
        else "2"
        if name == "Computing"
        else "11"
    )


def create_event(service, calendarId, name, room, details, start, end):
    event = {
        "summary": name,
        "location": room,
        "description": details,
        "start": {
            "dateTime": start,
            "timeZone": "Europe/London",
        },
        "end": {
            "dateTime": end,
            "timeZone": "Europe/London",
        },
        # colorId is the colour of the event on the calendar, it can be any number from 1-11
        "colorId": get_colorId(name),
    }

    event = service.events().insert(calendarId=calendarId, body=event).execute()
    return event


def update_event(service, calendarId, eventId, name, room, details, start, end):
    # First retrieve the event from the API.
    event = service.events().get(calendarId=calendarId, eventId=eventId).execute()

    event["summary"] = name
    event["location"] = room
    event["description"] = details
    event["start"] = {
        "dateTime": start,
        "timeZone": "Europe/London",
    }
    event["end"] = {
        "dateTime": end,
        "timeZone": "Europe/London",
    }
    event['colorId'] = get_colorId(name)

    updated_event = (
        service.events()
        .update(calendarId=calendarId, eventId=event["id"], body=event)
        .execute()
    )

    # Print the updated date.
    return updated_event


SCHOOL_CALENDAR = get_school_calendar()
