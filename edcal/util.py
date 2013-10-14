#!python3
from collections import defaultdict
from datetime import timedelta


def partition(partition_func, iterable):
    """Partition a list into named lists, based on a function of each element.
    """
    partitions = defaultdict(list)
    for element in iterable:
        partitions[partition_func(element)].append(element)
    return dict(partitions)


def first_weekday_after(weekday_index, date):
    """Returns a datetime for the first occurrence of weekday on
    or after the given date.

    Assumes 0 = Monday
    """
    return date + timedelta(days=date.weekday() + weekday_index)
