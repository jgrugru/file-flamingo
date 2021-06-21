from pytest import mark

from tests.fixtures import create_byte_file
from tests.fixtures import str_factory
from tests.fixtures import base_file, text_file  # noqa: F401
from tests.fixtures import env_setup_for_file_object  # noqa: F401
from tests.fixtures import TEST_FILE_LIST


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
        my_file = create_byte_file(file_path, contents_of_file)
    except IsADirectoryError:
        pass

    if my_file:
        assert my_file.filepath_exists()
        assert my_file.is_file() == is_file
    else:
        assert not is_file
