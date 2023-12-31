import get_events
import datetime
import os.path

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


def get_school_calendar(service):
    calendars = get_calendars(service)
    return [
        calendar for calendar in calendars["items"] if calendar["summary"] == "school"
    ][0]

def get_events_all(service,calendarId,start_date,end_date):
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

def create_event(service,calendarId,name,room,details,start,end):
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
        "colorId": "8" if name == "Supervised Study" else "7" if name == "Physics" else "6" if name == "Mathematic" else "2" if name == "Computing" else "11",
    }

    event = service.events().insert(calendarId=calendarId, body=event).execute()

def iso_to_datetime(iso_date_string):
    # Convert to datetime object
    try:
        dt_object = datetime.datetime.strptime(iso_date_string, '%Y-%m-%dT%H:%M:%SZ')

    # Add UTC timezone offset
        dt_with_utc_offset = dt_object.replace(tzinfo=datetime.timezone.utc)

    # Format as ISO 8601 with timezone offset
        iso8601_with_offset = dt_with_utc_offset.strftime('%Y-%m-%dT%H:%M:%S%z')
    except ValueError:
        iso8601_with_offset = iso_date_string
    return iso8601_with_offset


def get_all_events_from_satchel():
    start_date = datetime.datetime.now()
    add_to_calendar = {}
    for _ in range(10):
        events = get_events.get_events(AUTHORIZATION,USER_ID,start_date.strftime("%Y-%m-%d"))
        days = events['weeks'][0]['days']
        for day in days:
            if day['lessons'] == []:
                continue
            lessons = day['lessons']
            for lesson in lessons:
                #print(lesson)
                name = lesson['classGroup']['subject']
                start = lesson['period']['startDateTime']
                end = lesson['period']['endDateTime']

                room = lesson['room']
                teacher = lesson['teacher']
                teacher_name = f"{teacher['title']} {teacher['forename'][0]} {teacher['surname']}"
                details = f"{teacher_name} - {room}"

                # Needed to remove the "Supervised Study" events which clash with lessons
                try:
                    if add_to_calendar[start][3] == start and add_to_calendar[start][0] == "Supervised Study":
                        add_to_calendar[start] = [name,room,details,start,end]
                except KeyError:
                    add_to_calendar[start] = [name,room,details,start,end]
        start_date = start_date + datetime.timedelta(days=7)
    return add_to_calendar,start_date


def get_all_school_events():
    add_to_calendar = {}
    start_date = datetime.datetime.now()
    for _ in range(100):
        events = get_events.get_events(AUTHORIZATION,USER_ID,start_date.strftime("%Y-%m-%d"))

        school_events = events['weeks'][0]['events']
        for school_event in school_events:
            add_to_calendar[school_event['starts_at']] = [school_event['name'],"",school_event['event_type'],school_event['starts_at'],school_event['ends_at']]
        start_date = start_date + datetime.timedelta(days=7)

    return add_to_calendar,start_date


def remove_duplicates(service,events,end_date):
    
    # Gets all the events currently in the calendar and removes any pre-existing events from add_to_calendar
    # This is to prevent duplicate events
    old_events = get_events_all(service,SCHOOL_CALENDAR["id"],datetime.datetime.now(),end_date)
    for event in old_events:
        # Check if event is in add_to_calendar
        # if it is then remove it from add_to_calendar

        start_date = event['start']['dateTime']
        start_date = iso_to_datetime(start_date)[:-2]+":00"
        try:
            if events[start_date][3] == start_date:
                del events[start_date]
        except KeyError:
            pass
    return events

def add_events_to_calendar(service):
    add_to_calendar,end_date = get_all_events_from_satchel()
    add_to_calendar = remove_duplicates(service,add_to_calendar,end_date)
    print(add_to_calendar)
    # Adds all the events in add_to_calendar to the calendar
    for event in add_to_calendar.values():
        create_event(service,SCHOOL_CALENDAR["id"],*event)

    add_to_calendar,end_date = get_all_school_events()
    add_to_calendar = remove_duplicates(service,add_to_calendar,end_date)
    print(add_to_calendar)

    for event in add_to_calendar.values():
        create_event(service,SCHOOL_CALENDAR["id"],*event)




if __name__ == "__main__":
    service = get_service()
    SCHOOL_CALENDAR = get_school_calendar(service)
    add_events_to_calendar(service)