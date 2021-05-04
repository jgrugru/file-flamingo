from sys import path as syspath
from os import path
from pytest import mark

PARENT_DIR = path.abspath(path.join(path.dirname(__file__), path.pardir))
syspath.append(PARENT_DIR)

from tests.fixtures import text_file  # noqa: F401, E402

from fileflamingo.FileLines import strip_elements_of_list  # noqa: E402
from fileflamingo.FileLines import remove_whitespace_elements  # noqa: E402
from fileflamingo.FileLines import clean_elements_of_whitespace  # noqa: E402

from tests.fixtures import CONTENTS_OF_TEXT_FILE  # noqa: E402
from tests.fixtures import TEST_FILE_LINE_LIST  # noqa: E402


def test_text_file_init(text_file):  # noqa: F811
    assert text_file.filepath_exists()
    assert text_file.get_contents_of_file() == CONTENTS_OF_TEXT_FILE


def test_textfile_get_text_lines_as_list(text_file):  # noqa: F811
    my_list = text_file.get_text_lines_as_list()
    assert my_list == ['USERNAME=JGRUGRU', 'PASSWORD=12341515134$@#$^']


# def test_textfile_remove_blank_lines(text_file):
#     text_file.append_text_line_to_file("")
#     text_file.append_text_line_to_file("")
#     text_file.append_text_line_to_file("\n")
#     text_file.clean_lines_of_whitespace()
#     text_after_blank_lines_added = text_file.get_contents_of_file()
#     assert CONTENTS_OF_TEXT_FILE == text_after_blank_lines_added


# def test_textfile_write_text_lines_to_file(text_file):
#     print(text_file)
#     my_list = text_file.get_text_lines_as_list()
#     my_list.append("123512452315\n")
#     my_list.append("")
#     print(my_list)
#     text_file.write_text_lines_to_file(my_list)


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
