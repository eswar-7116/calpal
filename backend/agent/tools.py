from backend.gcal_tools.tools import *
from langchain.tools import tool
import dateparser

@tool
def is_slot_free(date: str, duration_minutes: int = 30) -> bool:
    """
    Checks if the given date has at least one free slot of the requested duration.

    Args:
        date (str): Date in 'YYYY-MM-DD' format.
        duration_minutes (int): Desired duration in minutes (default: 30).

    Returns:
        bool: True if a free slot exists, False otherwise.
    """
    return check_availability(date, duration_minutes)


@tool
def suggest_slots(date: str, duration_minutes: int = 30) -> list:
    """
    Suggests all available time slots on the given date for a meeting of the given duration.

    Args:
        date (str): Date in 'YYYY-MM-DD' format.
        duration_minutes (int): Duration of the meeting (default: 30 minutes)

    Returns:
        list: A list of available time slot tuples in (start, end) format.
    """
    return suggest_time_slots(date, duration_minutes)


@tool
def book_meeting(
        date: str,
        start_time: str,
        duration_minutes: int,
        title: str,
) -> dict:
    """
    Books an appointment on the connected Google Calendar.

    Args:
        date (str): Date of the meeting in 'YYYY-MM-DD' format.
        start_time (str): Start time in 'HH:MM' 24-hour format.
        duration_minutes (int): Duration in minutes.
        title (str): Title or summary of the event.

    Returns:
        dict: Confirmation info including event link, start time, etc.
    """
    return book_appointment(date, start_time, duration_minutes, title)

@tool
def resolve_datetime(text: str) -> str:
    """
    Converts a natural language date or time string into a standard datetime format.

    This tool helps the AI interpret phrases like:
    - "tomorrow at 4pm"
    - "next Friday"
    - "10-7-25"
    - "Monday 10am"

    Args:
        text (str): A natural language representation of date and time.

    Returns:
        str: ISO 8601 formatted datetime string (e.g., '2025-07-02T16:00:00').

    Example:
        resolve_datetime("tomorrow at 4pm") → "2025-07-02T16:00:00"
    """
    dt = dateparser.parse(text)
    if not dt:
        raise ValueError("Could not parse the given date/time.")
    return dt.isoformat()

tools = [is_slot_free, suggest_slots, book_meeting, resolve_datetime]
