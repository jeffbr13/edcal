#!python3
import re

from lxml import etree
import requests


class Course:
    """A course option presented on the T@Ed combined course selection page.

    :param code: Unique course university code, e.g. "MATH08005"
    :param title: Human-friendly name, e.g. "Calculus and its Applications".
    :param identifier: T@Ed system identifier, conveying the course code and semester information, e.g. "INFR08020_SV1_SEM2"
    """
    def __init__(self, code, title, identifier):
        self.code = code
        self.title = title
        self.identifier = identifier

    def __repr__(self):
        return '<Course: {0}>'.format(self.identifier)

    def __str__(self):
        return '<Course: {0} ({1})>'.format(self.title, self.code)



def combined_course_selection_page():
    return requests.post('https://www.ted.is.ed.ac.uk/UOE1314_SWS/demo_post2.asp', data={'student': 'N'}).content


def combined_course_selection_page_disk():
    with open('edcal/course-options.asp', 'rb') as f:
        return f.read()


def courses_from_page(course_page_content):
    html = etree.HTML(course_page_content)
    options = html.xpath('//select[@id="candidates"]/option')
    courses = []
    for option in options:
        identifier = option.get('value')
        course_code = identifier.split('_')[0]
        title = option.text.rsplit(' - ', maxsplit=1)[0].strip()
        courses.append(Course(course_code, title, identifier))
    return courses


def regex_filter(courses, regex_str):
    """Filters the list of courses by regex."""
    regex = re.compile(regex_str, flags=re.IGNORECASE)
    return [c for (c) in courses if (regex.search(c.code) or regex.search(c.title))]


def load_courses():
    try:
        return courses_from_page(combined_course_selection_page_disk())
    except FileNotFoundError:
        return courses_from_page(combined_course_selection_page())
