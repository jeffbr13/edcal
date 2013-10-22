#!python3
from collections import defaultdict
from datetime import timedelta


def classify(classifier_func, iterable):
    """Use a classification function to sort elements into a dict.

    :param classifier_func: returns an element's classification as a string
    :param iterable: collection of elements to classify
    """
    classifications = defaultdict(list)
    for element in iterable:
        classifications[classifier_func(element)].append(element)
    return dict(classifications)


def first_weekday_after(weekday_index, date):
    """Returns a datetime for the first occurrence of weekday on
    or after the given date.

    Assumes 0 = Monday
    """
    return date + timedelta(days=date.weekday() + weekday_index)
