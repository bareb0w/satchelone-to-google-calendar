import get_events
import datetime
import os.path
from google_utils import  get_service, get_school_calendar, get_all_events_from_google_calendar, create_event, update_event, check_if_event_exists
from satchel_utils import get_all_events_from_satchel


def iso_to_datetime(iso_date_string):
    # Convert to datetime object
    try:
        dt_object = datetime.datetime.strptime(iso_date_string, "%Y-%m-%dT%H:%M:%SZ")

        # Add UTC timezone offset
        dt_with_utc_offset = dt_object.replace(tzinfo=datetime.timezone.utc)

        # Format as ISO 8601 with timezone offset
        iso8601_with_offset = dt_with_utc_offset.strftime("%Y-%m-%dT%H:%M:%S%z")
    except ValueError:
        iso8601_with_offset = iso_date_string
    return iso8601_with_offset




def get_all_school_events():
    add_to_calendar = {}
    start_date = datetime.datetime.now()
    for _ in range(100):
        events = get_events.get_events(
            AUTHORIZATION, USER_ID, start_date.strftime("%Y-%m-%d")
        )

        school_events = events["weeks"][0]["events"]
        for school_event in school_events:
            add_to_calendar[school_event["starts_at"]] = [
                school_event["name"],
                "",
                school_event["event_type"],
                school_event["starts_at"],
                school_event["ends_at"],
            ]
        start_date = start_date + datetime.timedelta(days=7)

    return add_to_calendar, start_date


def process_events(service, events):
    # Checks if the event already exists in the calendar
    # If it does, it updates the event
    # If it doesn't, it creates the event
    for event in events.values():
        print(event)
        google_calendar_events = check_if_event_exists(service, SCHOOL_CALENDAR["id"], *event)
        if google_calendar_events == False:
            create_event(service, SCHOOL_CALENDAR["id"], *event)
            continue
        for gc_event in google_calendar_events:
            print("Updating event: ", gc_event["id"])
            print(update_event(service, SCHOOL_CALENDAR["id"], gc_event["id"], *event))



def add_lessons_to_calendar(service):
    add_to_calendar, _ = get_all_events_from_satchel()
    
    process_events(service, add_to_calendar)


def add_events_to_calendar(service):
    add_to_calendar, _ = get_all_school_events()
    process_events(service, add_to_calendar)



import os
from dotenv import load_dotenv

load_dotenv()

AUTHORIZATION = os.getenv("AUTHORIZATION")
USER_ID = os.getenv("USER_ID")
SCHOOL_ID = os.getenv("SCHOOL_ID")


if __name__ == "__main__":
    service = get_service()
    SCHOOL_CALENDAR = get_school_calendar(service)
    #add_events_to_calendar(service)
    add_lessons_to_calendar(service)
