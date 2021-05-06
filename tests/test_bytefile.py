from sys import path as syspath
from os import path
from pytest import mark

PARENT_DIR = path.abspath(path.join(path.dirname(__file__), path.pardir))

syspath.append(PARENT_DIR)

from tests.fixtures import create_byte_file_with_random_bytes  # noqa: E402
from tests.fixtures import str_factory  # noqa: E402
from tests.fixtures import base_file, text_file  # noqa: F401, E402
from tests.fixtures import env_setup_for_file_object  # noqa: F401, E402
from tests.fixtures import TEST_FILE_LIST  # noqa: E402'


@mark.parametrize("file_path, contents_of_file, is_file", [
    (TEST_FILE_LIST[0], bytes(str_factory(10), 'utf-8'), True),
    (TEST_FILE_LIST[1], bytes(str_factory(100), 'utf-8'), True),
    (TEST_FILE_LIST[2], bytes(str_factory(112), 'utf-8'), True),
    (TEST_FILE_LIST[3], bytes(str_factory(1), 'utf-8'), False),
    (TEST_FILE_LIST[4], bytes(str_factory(11), 'utf-8'), False),
    (TEST_FILE_LIST[5], bytes(str_factory(55), 'utf-8'), False),
    (TEST_FILE_LIST[6], bytes(str_factory(99), 'utf-8'), True),
    (TEST_FILE_LIST[7], bytes(str_factory(33), 'utf-8'), True),
    (TEST_FILE_LIST[8], bytes(str_factory(240), 'utf-8'), False),
    (TEST_FILE_LIST[9], bytes(str_factory(245), 'utf-8'), True),
])
def test_basefile_append_byte_line_to_file(env_setup_for_file_object,  # noqa: E501, F811
                                           file_path,
                                           contents_of_file,
                                           is_file):
    my_file = None
    try:
        my_file = create_byte_file_with_random_bytes(file_path,
                                                     contents_of_file)
    except IsADirectoryError:
        pass

    if my_file:
        assert my_file.filepath_exists()
        assert my_file.is_file() == is_file
    else:
        assert not is_file
