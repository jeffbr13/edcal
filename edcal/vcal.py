#!python3
from datetime import datetime, time
from time import strptime

from .ted.timetable import WEEKDAYS
from .util import first_weekday_after


class CalendarEvent:
    """Process and render a TimetableItem into an icalender VEVENT."""
    def __init__(self, timetable_item):
        self.timetable_item = timetable_item
        self.summary = timetable_item.name
        self.description = timetable_item.description
        self.location = ', '.join((timetable_item.room, timetable_item.building, 'University Of Edinburgh'))

        item_start_time = strptime(timetable_item.start, '%H:%M')
        self.first_item_start_time = datetime.combine(
            first_weekday_after(
                WEEKDAYS.index(timetable_item.weekday),
                timetable_item.minimum_date()),
            time(hour=item_start_time.tm_hour, minute=item_start_time.tm_min)
        )

        item_end_time = strptime(timetable_item.end, '%H:%M')
        self.first_item_end_time = datetime.combine(
                                          first_weekday_after(
                                                      WEEKDAYS.index(timetable_item.weekday),
                                                      timetable_item.minimum_date()),
                                          time(hour=item_end_time.tm_hour, minute=item_end_time.tm_min))

        self.series_end_time = timetable_item.maximum_date()

    def render(self, unique_id, now):
        return """BEGIN:VEVENT\r
UID:{unique_id}@edcal.benjeffrey.com\r
DTSTAMP:{now:%Y%m%dT%H%M%S}\r
SUMMARY:{summary}\r
DESCRIPTION:{description}\r
LOCATION:{location}\r
DTSTART;TZID=Europe/London:{first_start_time:%Y%m%dT%H%M%S}\r
DTEND;TZID=Europe/London:{first_end_time:%Y%m%dT%H%M%S}\r
RRULE:FREQ=WEEKLY;UNTIL={series_end_time}\r
END:VEVENT""".format(summary=self.summary, description=self.description,
        location=self.location,
        first_start_time=self.first_item_start_time,
        first_end_time=self.first_item_end_time,
        series_end_time=self.series_end_time,
        unique_id=unique_id,
        now=now)


def render_calendar(calendar_events, random_function, now):
    return """BEGIN:VCALENDAR\r
VERSION:2.0\r
PRODID:-//Ben Jeffrey/edcal//NONSGML v1.0//EN\r
{vevents}\r
END:VCALENDAR""".format(vevents='\r\n'.join([event.render(random_function(), now) for (event) in calendar_events]))
