from backend.gcal_tools.tools import *
from langchain.tools import tool

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

tools = [is_slot_free, suggest_slots, book_meeting]
