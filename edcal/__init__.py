#!python3
"""
edcal has two functional components:

1. Filtering the list of courses available to find their T@Ed identifiers
2. Making a request to T@Ed with the identifiers and parsing the result into an icalendar file.
"""
from datetime import datetime
from uuid import uuid4 as uuid

from .vcal import CalendarEvent, render_calendar
from .ted import timetable, courses





# def icalendar(course_identifiers):
#     timetable_items = timetable.timetable_items(timetable.fetch_webpage(course_identifiers))
#     event_series = timetable.by_name(timetable_items)

#     vevents = []
#     for event_name in event_series:
#         for event in event_series[event_name]:
#             vevents.append(CalendarEvent(event).render(uuid(), datetime.now))

#     return render_calendar(vevents)


cs = courses.courses_from_page(courses.combined_course_selection_page_disk())

sample_identifiers = [
    'INFR08020_SV1_SEM2',
    'INFR08012_SV1_SEM1',
    'INFR08015_SV1_SEM2',
    'INFR08013_SV1_SEM1',
    'INFR08014_SV1_SEM2']

print(courses.regex_search(cs, 'math'))
