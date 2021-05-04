"""
This file will hold all the helper functions that
can be used to manipulate file lines. The functions
will all return a list and accept a list as an argument.
"""


def strip_elements_of_list(file_lines):
    """
    Strips each element in list, removing whitespace from
    beginning and end of string.
    """
    return [line.strip() for line in file_lines]


def remove_whitespace_elements(file_lines):
    """
    Remove all elements of list that are only whitespace.
    """
    return list(filter(lambda x: x.strip() != '', file_lines))


def clean_elements_of_whitespace(file_lines):
    """
    Removes all unnecessary whitespace from the list.
    Strips each element followed by removing each
    element that is only whitespace.
    """
    file_lines = strip_elements_of_list(file_lines)
    file_lines = remove_whitespace_elements(file_lines)
    return file_lines


def map_file_lines(file_lines, fn):
    """
    Accepts a file_lines list and a function. Creates a new list with
    the contents passed through the funtion (fn).
    """
    return list(map(fn, file_lines))
