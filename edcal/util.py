#!python3
from collections import defaultdict


def partition(partition_func, iterable):
    """Partition a list into named lists, based on a function of each element.
    """
    partitions = defaultdict(list)
    for element in iterable:
        partitions[partition_func(element)].append(element)
    return dict(partitions)
