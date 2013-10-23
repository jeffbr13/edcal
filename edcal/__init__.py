#!python3
"""
edcal has two functional components:

1. Filtering the list of courses available to find their T@Ed identifiers
2. Making a request to T@Ed with the identifiers and parsing the result into an icalendar file.
"""
from datetime import datetime
from uuid import uuid4

from .ted.courses import load_courses, regex_filter
from .ted.timetable import fetch_timetable_items
from .vcal import CalendarEvent, render_calendar


class EdCal:
    """Interface for searching courses and building calendars."""
    def __init__(self):
        self.course_list = load_courses()

    def course_search(self, search_text):
        """Return a list of courses matching the given search text."""
        return regex_filter(self.course_list, search_text)

    def identifier_search(self, search_text):
        """Return a list of course identifiers for the given search text."""
        return [c.identifier for (c) in self.course_search(search_text)]


    def icalendar(self, identifiers):
        """Build and return an icalendar for the given course identifiers."""
        return render_calendar(
            [CalendarEvent(timetable_item) for (timetable_item) in fetch_timetable_items(identifiers)],
            uuid4,
            datetime.now()
        )
