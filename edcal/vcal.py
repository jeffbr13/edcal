#!python3
from collections import namedtuple
from datetime import datetime, time
from time import strptime

from .ted.courses import course_name
from .ted.timetable import (WEEKDAYS, first_weekday_after, minimum_date, maximum_date)


# CalendarEvent encodes the information for rendering an icalendar VEVENT:
CalendarEvent = namedtuple('CalendarEvent',
                           ['summary', 'description', 'location',
                            'first_start_time', 'first_end_time',
                            'series_end_time'])


def calendar_event(timetable_item):
    """Process a TimetableItem into a CalendarEvent"""
    summary = course_name(timetable_item)
    description = timetable_item.Description
    location = ', '.join((timetable_item.Room, timetable_item.Building, 'University Of Edinburgh'))

    item_start_time = strptime(timetable_item.Start, '%H:%M')
    first_start_time = datetime.combine(
                                        first_weekday_after(
                                                    WEEKDAYS.index(timetable_item.Day),
                                                    minimum_date(timetable_item)),
                                        time(hour=item_start_time.tm_hour, minute=item_start_time.tm_min))

    item_end_time = strptime(timetable_item.End, '%H:%M')
    first_end_time = datetime.combine(
                                      first_weekday_after(
                                                  WEEKDAYS.index(timetable_item.Day),
                                                  minimum_date(timetable_item)),
                                      time(hour=item_end_time.tm_hour, minute=item_end_time.tm_min))

    series_end_time = maximum_date(timetable_item)

    return CalendarEvent(summary=summary, description=description,
                         location=location, first_start_time=first_start_time,
                         first_end_time=first_end_time, series_end_time=series_end_time)


def render_event(calendar_event, unique_id, now):
    return """BEGIN:VEVENT\r
UID:{unique_id}@edcal.benjeffrey.com\r
DTSTAMP:{now:%Y%m%dT%H%M%S}\r
SUMMARY:{summary}\r
DESCRIPTION:{description}\r
LOCATION:{location}\r
DTSTART;TZID=Europe/London:{first_start_time:%Y%m%dT%H%M%S}\r
DTEND;TZID=Europe/London:{first_end_time:%Y%m%dT%H%M%S}\r
RRULE:FREQ=WEEKLY;UNTIL={series_end_time}\r
END:VEVENT""".format(summary=calendar_event.summary, description=calendar_event.description,
    location=calendar_event.location,
    first_start_time=calendar_event.first_start_time,
    first_end_time=calendar_event.first_end_time,
    series_end_time=calendar_event.series_end_time,
    unique_id=unique_id,
    now=now)


def render_all(events):
    return """BEGIN:VCALENDAR\r
VERSION:2.0\r
PRODID:-//Ben Jeffrey/edcal//NONSGML v1.0//EN\r
{vevents}\r
END:VCALENDAR""".format(vevents='\r\n'.join(events))
