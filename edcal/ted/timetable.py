#!python3
from collections import namedtuple
from datetime import date, timedelta
import re

from lxml import etree
import requests

from .courses import course_name
from ..util import partition


WEEKDAYS = ('MO','TU','WE','TH','FR','SA','SU')
# week numbers for queries
SEM1_WEEKS = list(range(17, 28))
SEM2_WEEKS = list(range(34, 39)) + list(range(40, 46))


SEM1_PATTERN = re.compile('Sem1', flags=re.IGNORECASE)
SEM2_PATTERN = re.compile('Sem2', flags=re.IGNORECASE)

# 2013/14 semester dates
SEM1_START = date(2013, 9, 16)
SEM1_END = date(2013, 12, 1)
SEM2_START = date(2014, 1, 13)
SEM2_END = date(2014, 4, 6)

# TimetableItem encodes a T@Ed timetable row for easier field access:
TimetableItem = namedtuple('TimetableItem',
                           ['Day', 'Activity', 'Description', 'Type',
                           'Start', 'End', 'Weeks', 'Building', 'Room', 'Staff'])


def fetch_webpage(courses, week_numbers):
    request_args = {
        'combined': 'on',
        'objectclass': 'module',
        'style': 'textspreadsheet',
        'template': 'SWSCUST Object Textspreadsheet',
        'week': ';'.join(map(str, week_numbers)),
        'identifier': ', '.join([course.identifier for (course) in courses])
    }
    return requests.post('https://www.ted.is.ed.ac.uk/UOE1213_SWS/timetable.asp', data=request_args).content


def timetable_items(page_content):
    html = etree.HTML(page_content)
    days = zip(WEEKDAYS, html.xpath('//table[@class="spreadsheet"]'))

    items = []
    for (weekday, table) in days:
        trs = table.xpath('.//tr[not(@class)][./td]')
        for row in trs:
            items.append(TimetableItem(weekday, *row.xpath('./td//text()')))

    return items


def minimum_date(item):
    """Date of the first day of the first semester of the item."""
    if SEM1_PATTERN.match(item.Weeks):
        return SEM1_START
    else:
        return SEM2_START


def maximum_date(timetable_item):
    """Date of the last day of the last semester of the timetable_item."""
    if SEM2_PATTERN.match(timetable_item.Weeks):
        return SEM2_END
    else:
        return SEM1_END


def first_weekday_after(weekday_index, date):
    """Returns a datetime for the first occurrence of weekday on
    or after the given date.
    Assumes 0 = Monday
    """
    return date + timedelta(days=date.weekday() + weekday_index)


def by_name(items):
    return partition(lambda item: course_name(item), items)
