from os import chdir, path
from pytest import mark

from fileflamingo.ByteFile import ByteFile
from fileflamingo.BaseFile import BaseFile
from tests.fixtures import create_file
from tests.fixtures import create_base_file
from tests.fixtures import create_text_file_with_random_str
from tests.fixtures import base_file, text_file  # noqa: F401
from tests.fixtures import env_setup_for_file_object  # noqa: F401
from tests.fixtures import CONTENTS_OF_TEXT_FILE
from tests.fixtures import TEST_FILE_LIST
from tests.fixtures import TEST_FILE_LINE_LIST

class Test_BaseFile():
    def setup_class(cls, tmp_path):
        chdir(tmp_path)

    @mark.parametrize(
        "file_path, is_file",
        [
            ("env_path/.env", True),
            ("./env_path/env", True),
            (".env_path/env", True),
            ("env_path/env/", False),
            (".env_path/env/", False),
            ("././././env1/", False),
            ("././././env2", True),
            ("../env_path/.env", True),
            ("./env_path1/.env/", True),
            ("env.txt", True),
        ],
    )
    def test_basefile_create_filepath(self, file_path, is_file):
        my_file = BaseFile(file_path)
        my_file.create_filepath()
        print("\n" + my_file.filepath)
        if(my_file.is_file()):
            print(f"{my_file} is file")
        else:
            print(f"{my_file} is dir")
        # assert my_file.filepath_exists()
        # assert my_file.is_file() == is_file


# @mark.parametrize(
#     "file_path, exception_raised",
#     [
#         (TEST_FILE_LIST[0], False),
#         (TEST_FILE_LIST[1], False),
#         (TEST_FILE_LIST[2], False),
#         (TEST_FILE_LIST[3], True),
#         (TEST_FILE_LIST[4], True),
#         (TEST_FILE_LIST[5], True),
#         (TEST_FILE_LIST[6], False),
#         (TEST_FILE_LIST[7], False),
#         (TEST_FILE_LIST[8], True),
#         (TEST_FILE_LIST[9], False),
#     ],
# )
# def test_basefile_delete_filepath(
#     env_setup_for_file_object, file_path, exception_raised  # noqa: F811
# ):
#     my_file = create_base_file(file_path)

#     was_exception_raised = False
#     try:
#         my_file.delete_file()
#     except (FileNotFoundError, IsADirectoryError):
#         was_exception_raised = True

#     assert was_exception_raised == exception_raised


# @mark.parametrize(
#     "file_path, creates_file, exception_raised",
#     [
#         (TEST_FILE_LIST[0], True, False),
#         (TEST_FILE_LIST[3], True, True),
#         (TEST_FILE_LIST[0], False, True),
#     ],
# )
# def test_basefile_clear_file(
#     env_setup_for_file_object, creates_file, file_path, exception_raised  # noqa: F811
# ):
#     my_file = create_base_file(file_path, create_filepath=creates_file)

#     was_exception_raised = False
#     try:
#         my_file.clear_file()
#     except (FileNotFoundError, IsADirectoryError):
#         was_exception_raised = True

#     assert was_exception_raised == exception_raised


# def test_basefile_clear_file_doesnt_create_file(tmp_path):
#     my_file = create_base_file(
#         path.join(tmp_path, "testing.txt"), create_filepath=False
#     )
#     try:
#         my_file.clear_file()
#     except (FileNotFoundError, IsADirectoryError):
#         pass
#     assert not my_file.filepath_exists()


# @mark.parametrize(
#     "file_path, contents_of_file, \
#                   creates_file, expected_output",
#     [
#         (TEST_FILE_LIST[0], None, True, False),
#         (TEST_FILE_LIST[3], None, True, False),
#         (TEST_FILE_LIST[0], None, False, False),
#         (TEST_FILE_LIST[0], b"\x00\x01\xffsd", True, True),
#     ],
# )
# def test_basefile_is_binary(
#     env_setup_for_file_object,  # noqa: F811
#     file_path,
#     creates_file,
#     contents_of_file,
#     expected_output,
# ):
#     my_file = create_file(ByteFile, file_path)
#     if creates_file:
#         my_file.create_filepath()
#     if contents_of_file:
#         my_file.write_bytes_to_file(contents_of_file)
#     result = my_file.is_binary()

#     assert result == expected_output


# @mark.parametrize(
#     "filepath, expected_result",
#     [
#         (TEST_FILE_LIST[0], False),
#         (TEST_FILE_LIST[1], False),
#         (TEST_FILE_LIST[2], False),
#         (TEST_FILE_LIST[3], True),
#         (TEST_FILE_LIST[4], True),
#         (TEST_FILE_LIST[5], True),
#         (TEST_FILE_LIST[6], False),
#         (TEST_FILE_LIST[7], False),
#         (TEST_FILE_LIST[8], True),
#         (TEST_FILE_LIST[9], False),
#     ],
# )
# def test_basefile_is_empty(
#     env_setup_for_file_object, filepath, expected_result  # noqa: F811
# ):
#     result = False
#     try:
#         my_file = create_text_file_with_random_str(filepath)
#         result = my_file.is_empty()
#     except IsADirectoryError:
#         expected_result = False
#     assert result == expected_result


# @mark.parametrize(
#     "filepath, create_file, expected_result",
#     [
#         (TEST_FILE_LIST[0], True, True),
#         (TEST_FILE_LIST[1], True, True),
#         (TEST_FILE_LIST[2], True, True),
#         (TEST_FILE_LIST[3], True, True),
#         (TEST_FILE_LIST[4], False, False),
#         (TEST_FILE_LIST[5], True, True),
#         (TEST_FILE_LIST[6], True, True),
#         (TEST_FILE_LIST[7], True, True),
#         (TEST_FILE_LIST[8], False, False),
#         (TEST_FILE_LIST[9], True, True),
#     ],
# )
# def test_basefile_filepath_exists(
#     env_setup_for_file_object, create_file, filepath, expected_result  # noqa: F811
# ):
#     my_file = create_base_file(filepath, create_filepath=create_file)
#     result = my_file.filepath_exists()
#     assert result == expected_result


# def test_basefile_get_contents_of_text_file(text_file):  # noqa: F811
#     assert text_file.get_contents_of_file() == CONTENTS_OF_TEXT_FILE


# @mark.parametrize(
#     "my_list, expected_output",
#     [
#         (TEST_FILE_LINE_LIST[0], ["", "asdfasd", "", "asdfadsf"]),
#         (TEST_FILE_LINE_LIST[1], ["", "", "", "asdfadsf"]),
#     ],
# )
# def test_basefile_strip_elements_of_list(my_list, expected_output):
#     my_file = create_base_file("test.txt", create_filepath=False)
#     my_list = my_file.strip_elements_of_list(my_list)
#     assert expected_output == my_list


# @mark.parametrize(
#     "my_list, expected_output",
#     [
#         (TEST_FILE_LINE_LIST[0], ["asdfasd", "asdfadsf\n"]),
#         (TEST_FILE_LINE_LIST[1], ["asdfadsf\n"]),
#     ],
# )
# def test_basefile_remove_whitespace_elements(my_list, expected_output):
#     my_file = create_base_file("test.txt", create_filepath=False)
#     my_list = my_file.remove_whitespace_elements(my_list)
#     assert expected_output == my_list


# @mark.parametrize(
#     "my_list, expected_output",
#     [
#         (TEST_FILE_LINE_LIST[0], ["asdfasd", "asdfadsf"]),
#         (TEST_FILE_LINE_LIST[1], ["asdfadsf"]),
#     ],
# )
# def test_basefile_clean_elements_of_whitespace(my_list, expected_output):
#     my_file = create_base_file("test.txt", create_filepath=False)
#     my_list = my_file.clean_elements_of_whitespace(my_list)
#     assert expected_output == my_list


# def test_basefile_str(base_file):  # noqa: F811
#     assert base_file.get_filepath() == str(base_file)
