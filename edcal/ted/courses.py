#!python3
from collections import namedtuple

from lxml import etree
import requests


# Encodes {course code}_{unknown}_{session}, e.g. 'INFR08020_SV1_SEM2_weeks'
Course = namedtuple('Course', ['code', 'title', 'identifier'])


def fetch_webpage():
    return requests.post('https://www.ted.is.ed.ac.uk/UOE1314_SWS/demo_post2.asp', data={'student': 'N'}).content


def load_saved_webpage():
    with open('course-options', 'rb') as f:
        return f.read()


def courses_from_page(course_page_content):
    html = etree.HTML(course_page_content)
    options = html.xpath('//select[@id="candidates"]/option')
    courses = []
    for option in options:
        identifier = option.get('value')
        course_code = identifier.split('_')[0]
        title = option.text.rsplit(' - ', maxsplit=1)[0]
        courses.append(Course(course_code, title, identifier))
    return courses


def course_name(timetable_item):
    return timetable_item.Activity.split('_')[0].rsplit('/')[0]
