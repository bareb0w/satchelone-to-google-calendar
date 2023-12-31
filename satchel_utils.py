from datetime import datetime, timedelta
import requests

import os
from dotenv import load_dotenv

load_dotenv()

AUTHORIZATION = os.getenv("AUTHORIZATION")
USER_ID = os.getenv("USER_ID")
SCHOOL_ID = os.getenv("SCHOOL_ID")


def get_events(
    authorization, user_id, school_id, start_date=datetime.now().strftime("%Y-%m-%d")
):
    headers = {
        "authority": "api.satchelone.com",
        "accept": "application/smhw.v2021.5+json",
        "accept-language": "en-GB,en;q=0.8",
        "authorization": authorization,
        "content-type": "application/json",
        "origin": "https://www.satchelone.com",
        "referer": "https://www.satchelone.com/",
        "sec-ch-ua": '"Not_A Brand";v="8", "Chromium";v="120", "Brave";v="120"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Linux"',
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-site",
        "sec-gpc": "1",
        "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "x-platform": "web",
    }

    params = {
        "requestDate": start_date,
    }

    response = requests.get(
        f"https://api.satchelone.com/api/timetable/school/{school_id}/student/{user_id}",
        params=params,
        headers=headers,
    )
    return response.json()


def process_all_lessons(lessons, add_to_calendar):
    for lesson in lessons:
        # print(lesson)
        name = lesson["classGroup"]["subject"]
        start = lesson["period"]["startDateTime"]
        end = lesson["period"]["endDateTime"]

        room = lesson["room"]
        teacher = lesson["teacher"]
        teacher_name = (
            f"{teacher['title']} {teacher['forename'][0]} {teacher['surname']}"
        )
        details = f"{teacher_name} - {room}"

        # Needed to remove the "Supervised Study" events which clash with lessons
        try:
            if (
                add_to_calendar[start][3] == start
                and add_to_calendar[start][0] == "Supervised Study"
            ):
                add_to_calendar[start] = [name, room, details, start, end]
        except KeyError:
            add_to_calendar[start] = [name, room, details, start, end]
    return add_to_calendar


def get_all_events_from_satchel():
    start_date = datetime.now()
    add_to_calendar = {}
    for _ in range(10):
        events = get_events(
            AUTHORIZATION, USER_ID, SCHOOL_ID, start_date.strftime("%Y-%m-%d")
        )
        days = events["weeks"][0]["days"]
        for day in days:
            if day["lessons"] == []:
                continue
            lessons = day["lessons"]
            add_to_calendar = process_all_lessons(lessons, add_to_calendar)
            print(add_to_calendar)
        start_date = start_date + timedelta(days=7)

    # start_date is now the date of the last lesson
    return add_to_calendar, start_date


def get_all_school_events():
    add_to_calendar = {}
    start_date = datetime.datetime.now()
    for _ in range(100):
        events = get_events(AUTHORIZATION, USER_ID, start_date.strftime("%Y-%m-%d"))

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
