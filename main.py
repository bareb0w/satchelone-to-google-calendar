from google_utils import (
    get_service,
    get_school_calendar,
    create_event,
    update_event,
    check_if_event_exists,
)
from satchel_utils import (
    get_all_events_from_satchel, 
    get_all_school_events,
)


def process_events(service, events):
    # Checks if the event already exists in the calendar
    # If it does, it updates the event
    # If it doesn't, it creates the event
    for event in events.values():
        google_calendar_events = check_if_event_exists(
            service, SCHOOL_CALENDAR["id"], *event
        )
        if google_calendar_events == False:
            create_event(service, SCHOOL_CALENDAR["id"], *event)
            continue
        for gc_event in google_calendar_events:
            # print("Updating event: ", gc_event["id"])
            # print(
            update_event(service, SCHOOL_CALENDAR["id"], gc_event["id"], *event)  # )


def add_lessons_to_calendar(service):
    add_to_calendar, _ = get_all_events_from_satchel()
    process_events(service, add_to_calendar)


def add_events_to_calendar(service):
    add_to_calendar, _ = get_all_school_events()
    process_events(service, add_to_calendar)


if __name__ == "__main__":
    service = get_service()
    SCHOOL_CALENDAR = get_school_calendar(service)
    # add_events_to_calendar(service)
    add_lessons_to_calendar(service)
