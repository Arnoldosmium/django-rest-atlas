"""
:author Arnold Lin
A collection of utility functions
"""


def fulfill_or_throw(cond, what):
    """
    Check condition and otherwise throw exception class
    :param cond: boolean condition
    :param what: instantiated exception
    :return: None
    """
    if not cond:
        raise what
