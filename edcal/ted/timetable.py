#!python3
from datetime import date
import re

from lxml import etree
import requests

from ..util import partition


WEEKDAYS = ('MO','TU','WE','TH','FR','SA','SU')
# week numbers for queries
SEM1_WEEKS = list(range(17, 28))
SEM2_WEEKS = list(range(34, 39)) + list(range(40, 46))
SEM1_AND_SEM2_WEEKS = SEM1_WEEKS + SEM2_WEEKS


SEM1_PATTERN = re.compile('Sem1', flags=re.IGNORECASE)
SEM2_PATTERN = re.compile('Sem2', flags=re.IGNORECASE)

# 2013/14 semester dates
SEM1_START = date(2013, 9, 16)
SEM1_END = date(2013, 12, 1)
SEM2_START = date(2014, 1, 13)
SEM2_END = date(2014, 4, 6)


class TimetableItem:
    """A T@ED rendered timetable row.

    :param weekday: Two-letter upper-case string, e.g. "MO"
    """
    def __init__(self, weekday, activity, description, activity_type, start, end, weeks, building, room, staff):
        self.weekday = weekday

        # Information directly from the webpage:
        self.activity = activity
        self.description = description
        self.type = activity_type
        self.start = start
        self.end = end
        self.weeks = weeks
        self.building = building
        self.room = room
        self.staff = staff

        # Human-friendly course name:
        self.name = self.activity.split('_')[0].rsplit('/')[0]


    def minimum_date(self):
        """Date of the first day of the first semester of the item."""
        if SEM1_PATTERN.match(self.weeks):
            return SEM1_START
        else:
            return SEM2_START


    def maximum_date(self):
        """Date of the last day of the last semester of the timetable_item."""
        if SEM2_PATTERN.match(self.weeks):
            return SEM2_END
        else:
            return SEM1_END


def fetch_webpage(course_identifiers, week_numbers=SEM1_AND_SEM2_WEEKS):
    request_args = {
        'combined': 'on',
        'objectclass': 'module',
        'style': 'textspreadsheet',
        'template': 'SWSCUST Object Textspreadsheet',
        'week': ';'.join(map(str, week_numbers)),
        'identifier': ', '.join(course_identifiers)
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


def fetch_timetable_items(course_identifiers, week_numbers=SEM1_AND_SEM2_WEEKS):
    return timetable_items(fetch_webpage(course_identifiers, week_numbers))


def by_name(timetable_items):
    return partition((lambda item: item.name), timetable_items)
