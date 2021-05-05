from sys import path as syspath
from os import path
from pytest import mark

PARENT_DIR = path.abspath(path.join(path.dirname(__file__), path.pardir))

syspath.append(PARENT_DIR)

from fileflamingo.ByteFile import ByteFile  # noqa: E402
from tests.fixtures import create_file  # noqa: E402
from tests.fixtures import create_base_file  # noqa: E402
from tests.fixtures import base_file, text_file  # noqa: F401, E402
from tests.fixtures import env_setup_for_file_object  # noqa: F401, E402
from tests.fixtures import CONTENTS_OF_TEXT_FILE  # noqa: E402
from tests.fixtures import TEST_FILE_LIST  # noqa: E402


@mark.parametrize("file_path, is_file", [
    (TEST_FILE_LIST[0], True),
    (TEST_FILE_LIST[1], True),
    (TEST_FILE_LIST[2], True),
    (TEST_FILE_LIST[3], False),
    (TEST_FILE_LIST[4], False),
    (TEST_FILE_LIST[5], False),
    (TEST_FILE_LIST[6], True),
    (TEST_FILE_LIST[7], True),
    (TEST_FILE_LIST[8], False),
    (TEST_FILE_LIST[9], True),
])
def test_basefile_create_filepath(env_setup_for_file_object,  # noqa: F811
                                  file_path,
                                  is_file):
    my_file = create_base_file(file_path)
    assert my_file.filepath_exists()
    assert my_file.is_file() == is_file


@mark.parametrize("file_path, exception_raised", [
    (TEST_FILE_LIST[0], False),
    (TEST_FILE_LIST[1], False),
    (TEST_FILE_LIST[2], False),
    (TEST_FILE_LIST[3], True),
    (TEST_FILE_LIST[4], True),
    (TEST_FILE_LIST[5], True),
    (TEST_FILE_LIST[6], False),
    (TEST_FILE_LIST[7], False),
    (TEST_FILE_LIST[8], True),
    (TEST_FILE_LIST[9], False),

])
def test_basefile_delete_filepath(env_setup_for_file_object,   # noqa: F811
                                  file_path,
                                  exception_raised):
    my_file = create_base_file(file_path)

    was_exception_raised = False
    try:
        my_file.delete_file()
    except (FileNotFoundError, IsADirectoryError):
        was_exception_raised = True

    assert was_exception_raised == exception_raised


@mark.parametrize("file_path, creates_file, exception_raised", [
    (TEST_FILE_LIST[0], True, False),
    (TEST_FILE_LIST[3], True, True),
    (TEST_FILE_LIST[0], False, True),
])
def test_basefile_clear_file(env_setup_for_file_object,   # noqa: F811
                             creates_file,
                             file_path,
                             exception_raised):
    my_file = create_base_file(file_path, create_filepath=creates_file)

    was_exception_raised = False
    try:
        my_file.clear_file()
    except (FileNotFoundError, IsADirectoryError):
        was_exception_raised = True

    assert was_exception_raised == exception_raised


def test_basefile_clear_file_doesnt_create_file(tmp_path):
    my_file = create_base_file(path.join(tmp_path, 'testing.txt'),
                               create_filepath=False)
    try:
        my_file.clear_file()
    except (FileNotFoundError, IsADirectoryError):
        pass
    assert not my_file.filepath_exists()


@mark.parametrize("file_path, contents_of_file, \
                  creates_file, expected_output", [
    (TEST_FILE_LIST[0], None, True, False),
    (TEST_FILE_LIST[3], None, True, False),
    (TEST_FILE_LIST[0], None, False, False),
    (TEST_FILE_LIST[0], b'\x00\x01\xffsd', True, True),
])
def test_basefile_is_binary(env_setup_for_file_object,   # noqa: F811
                            file_path,
                            creates_file,
                            contents_of_file,
                            expected_output):
    my_file = create_file(ByteFile, file_path)
    if creates_file:
        my_file.create_filepath()
    if contents_of_file:
        my_file.write_bytes_to_file(contents_of_file)
    result = my_file.is_binary()

    assert result == expected_output


def test_basefile_get_contents_of_text_file(text_file):  # noqa: F811
    assert text_file.get_contents_of_file() == CONTENTS_OF_TEXT_FILE


def test_basefile_str(base_file):  # noqa: F811
    assert base_file.get_filepath() == str(base_file)
