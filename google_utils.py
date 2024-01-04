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


def adjust_time_datetime(start, end):
    if end.hour == 10:
        # print("Lesson 2")
        start = start.replace(hour=10, minute=20)
        end = end.replace(hour=11, minute=20)

    elif end.hour == 12:
        # print("Lesson 4")
        start = start.replace(hour=13, minute=0)
        end = end.replace(hour=14, minute=0)
    return start, end


def check_if_event_exists(service, calendarId, name, room, details, start, end):
    # converts the following date format into a datetime object
    # 2024-01-18T12:20:00+00:00

    end = convert_to_datetime(end)
    start = convert_to_datetime(start)

    events = get_all_events_from_google_calendar(service, calendarId, start, end)
    # start, end = adjust_time_datetime(start, end)
    # events2 = get_all_events_from_google_calendar(service, calendarId, start, end)
    if events == []:
        return False
    else:
        return events


def get_colorId(name):
    import dotenv
    import os

    dotenv.load_dotenv()
    colorid_lookup = os.getenv("COLORID")
    if colorid_lookup is None:
        return "11"
    colorid_lookup = eval(colorid_lookup)
    # print(colorid_lookup)
    if name in colorid_lookup:
        return colorid_lookup[name]

    return "11"


def create_event(service, calendarId, name, room, details, start, end):
    start, end = adjust_time(start, end)
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


def adjust_time(start, end):
    # print(start.split(":")[0].split("T")[1])
    # print(end[-14:])
    if "10:00:00+00:00" == start[-14:]:
        # print("Lesson 2")
        start = start.replace("10:00:00+00:00", "10:20:00+00:00")
        end = end.replace("11:00:00+00:00", "11:20:00+00:00")
    elif "12:20:00+00:00" == start[-14:]:
        # print("Lesson 4")
        start = start.replace("12:20:00+00:00", "13:00:00+00:00")
        end = end.replace("13:20:00+00:00", "14:00:00+00:00")
    return start, end


def update_event(service, calendarId, eventId, name, room, details, start, end):
    start, end = adjust_time(start, end)

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
    event["colorId"] = get_colorId(name)

    updated_event = (
        service.events()
        .update(calendarId=calendarId, eventId=event["id"], body=event)
        .execute()
    )

    # Print the updated date.
    return updated_event


SCHOOL_CALENDAR = get_school_calendar()
