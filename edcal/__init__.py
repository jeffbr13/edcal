#!python3
from datetime import datetime
from uuid import uuid4 as uuid

from .vcal import calendar_event, render_all, render_event
from .ted import timetable


def icalendar(courses, weeks):
    timetable_items = timetable.timetable_items(timetable.fetch_webpage(courses, weeks))
    event_series = timetable.by_name(timetable_items)

    vevents = []
    for event_name in event_series:
        for event in event_series[event_name]:
            vevents.append(render_event(calendar_event(event), uuid(), datetime.now))

    return render_all(vevents)
