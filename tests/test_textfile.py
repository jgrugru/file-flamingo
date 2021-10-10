from tests.fixtures import text_file  # noqa: F401
from tests.fixtures import CONTENTS_OF_TEXT_FILE


def test_text_file_init(text_file):  # noqa: F811
    assert text_file.filepath_exists()
    assert text_file.get_contents_of_file() == CONTENTS_OF_TEXT_FILE


def test_textfile_get_text_lines_as_list(text_file):  # noqa: F811
    my_list = text_file.get_text_lines_as_list()
    assert my_list == ["USERNAME=JGRUGRU", "PASSWORD=12341515134$@#$^"]


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
