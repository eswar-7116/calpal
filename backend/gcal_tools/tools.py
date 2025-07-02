import os
from datetime import datetime, timedelta

import pytz
from google.oauth2 import service_account
from googleapiclient.discovery import build

SERVICE_ACCOUNT_FILE = "backend/credentials/calpal_service_acc_creds.json"
CALENDAR_ID = os.getenv("CALENDAR_ID")
TIMEZONE = "Asia/Kolkata"

creds = service_account.Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE,
    scopes=["https://www.googleapis.com/auth/calendar"]
)
service = build("calendar", "v3", credentials=creds)


def check_availability(date: str, duration_minutes: int = 30) -> bool:
    tz = pytz.timezone(TIMEZONE)
    start = tz.localize(datetime.strptime(date + "T09:00:00", "%Y-%m-%dT%H:%M:%S"))
    end = tz.localize(datetime.strptime(date + "T17:00:00", "%Y-%m-%dT%H:%M:%S"))

    body = {
        "timeMin": start.isoformat(),
        "timeMax": end.isoformat(),
        "items": [{"id": CALENDAR_ID}]
    }

    events = service.freebusy().query(body=body).execute()
    busy_times = events["calendars"][CALENDAR_ID]["busy"]

    current = start
    while current + timedelta(minutes=duration_minutes) <= end:
        slot_end = current + timedelta(minutes=duration_minutes)
        overlap = any(
            current < datetime.fromisoformat(b['end']) and slot_end > datetime.fromisoformat(b['start'])
            for b in busy_times
        )
        if not overlap:
            return True
        current += timedelta(minutes=15)

    return False


def suggest_time_slots(date: str, duration_minutes: int = 30, interval_minutes: int = 30) -> list:
    tz = pytz.timezone(TIMEZONE)
    start_time = tz.localize(datetime.strptime(date + 'T09:00:00', '%Y-%m-%dT%H:%M:%S'))
    end_time = tz.localize(datetime.strptime(date + 'T17:00:00', '%Y-%m-%dT%H:%M:%S'))

    body = {
        "timeMin": start_time.isoformat(),
        "timeMax": end_time.isoformat(),
        "items": [{"id": CALENDAR_ID}]
    }

    events = service.freebusy().query(body=body).execute()
    busy_slots = events['calendars'][CALENDAR_ID]['busy']

    free_slots = []
    current = start_time

    while current + timedelta(minutes=duration_minutes) <= end_time:
        slot_end = current + timedelta(minutes=duration_minutes)
        conflict = any(
            current < datetime.fromisoformat(b['end']) and slot_end > datetime.fromisoformat(b['start'])
            for b in busy_slots
        )
        if not conflict:
            free_slots.append((current.strftime('%H:%M'), slot_end.strftime('%H:%M')))
        current += timedelta(minutes=interval_minutes)

    return free_slots


def book_appointment(date: str, start_time: str, duration_minutes: int, title: str):
    tz = pytz.timezone(TIMEZONE)
    start = tz.localize(datetime.strptime(f"{date}T{start_time}", '%Y-%m-%dT%H:%M'))
    end = start + timedelta(minutes=duration_minutes)

    event = {
        'summary': title,
        'start': {'dateTime': start.isoformat(), 'timeZone': TIMEZONE},
        'end': {'dateTime': end.isoformat(), 'timeZone': TIMEZONE},
    }

    event = service.events().insert(calendarId=CALENDAR_ID, body=event).execute()
    return {
        "status": "success",
        "event_link": event.get("htmlLink"),
        "start": start.strftime('%Y-%m-%d %H:%M'),
        "title": title
    }
