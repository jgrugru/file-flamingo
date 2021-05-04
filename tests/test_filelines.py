from sys import path as syspath
from os import path
from pytest import mark

PARENT_DIR = path.abspath(path.join(path.dirname(__file__), path.pardir))
syspath.append(PARENT_DIR)

from fileflamingo.FileLines import strip_elements_of_list  # noqa: E402
from fileflamingo.FileLines import remove_whitespace_elements  # noqa: E402
from fileflamingo.FileLines import clean_elements_of_whitespace  # noqa: E402
from tests.fixtures import TEST_FILE_LINE_LIST  # noqa: E402


@mark.parametrize("my_list, expected_output", [
    (TEST_FILE_LINE_LIST[0], ['', 'asdfasd', '', 'asdfadsf']),
    (TEST_FILE_LINE_LIST[1], ['', '', '', 'asdfadsf']),
])
def test_filelines_strip_elements_of_list(my_list, expected_output):
    my_list = strip_elements_of_list(my_list)
    assert expected_output == my_list


@mark.parametrize("my_list, expected_output", [
    (TEST_FILE_LINE_LIST[0], ['asdfasd', 'asdfadsf\n']),
    (TEST_FILE_LINE_LIST[1], ['asdfadsf\n']),
])
def test_filelines_remove_whitespace_elements(my_list, expected_output):
    my_list = remove_whitespace_elements(my_list)
    assert expected_output == my_list


@mark.parametrize("my_list, expected_output", [
    (TEST_FILE_LINE_LIST[0], ['asdfasd', 'asdfadsf']),
    (TEST_FILE_LINE_LIST[1], ['asdfadsf']),
])
def test_filelines_clean_elements_of_whitespace(my_list, expected_output):
    my_list = clean_elements_of_whitespace(my_list)
    assert expected_output == my_list
