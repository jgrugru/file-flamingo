import sys
from os import path, chdir
from pytest import fixture, mark, fail

sys.path.append(path.abspath(path.join(path.dirname(__file__),
                path.pardir)))

from fileflamingo.BaseFile import BaseFile              # noqa: E402
from fileflamingo.RSAFile import RSAFile                # noqa: E402
from fileflamingo.EncryptionFile import EncryptionFile  # noqa: E402
from fileflamingo.TextFile import TextFile              # noqa: E402

TEST_FILE_LIST = [
    "env_path/.env",
    "./env_path/env",
    ".env_path/env",
    "env_path/env/",
    ".env_path/env/",
    "././././env/",
    "././././env",
    "../env_path/.env",
    "../env_path1/.env/"]


def create_file(fileclass, filepath, *args, **kwargs):
    my_file = fileclass(filepath, *args, **kwargs)
    my_file.create_filepath()
    return my_file


@fixture
def base_file(tmp_path):
    my_file = create_file(BaseFile, path.join(tmp_path, 'test.txt'))
    return my_file


@fixture
def text_file(tmp_path):
    my_file = create_file(
        TextFile,
        path.join(tmp_path, 'test.txt'),
        txt="0123456789")
    return my_file


@fixture
def rsa_file(tmp_path):
    my_rsa_file = create_file(RSAFile, path.join(tmp_path, 'my_key.pem'))
    my_rsa_file.gen_pem_file()
    return my_rsa_file


@fixture
def encryption_file(text_file, rsa_file):
    my_encrypytion_file = create_file(
        EncryptionFile,
        text_file,
        rsa_file)
    return my_encrypytion_file


@fixture
def large_txt_file():
    return BaseFile(path.abspath(path.join(path.dirname(__file__),
                    'test.txt')))


@fixture
def env_setup_for_file_object(tmp_path):
    chdir(tmp_path)


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
])
def test_basefile_create_filepath(env_setup_for_file_object,
                                  file_path,
                                  is_file):
    my_file = create_file(BaseFile, file_path)
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
])
def test_basefile_delete_filepath(env_setup_for_file_object,
                                  file_path,
                                  exception_raised):
    my_file = create_file(BaseFile, file_path)

    was_exception_raised = False
    try:
        my_file.delete_file()
    except FileNotFoundError:
        was_exception_raised = True
    except IsADirectoryError:
        was_exception_raised = True

    assert was_exception_raised == exception_raised


@mark.parametrize("file_path, create_filepath, exception_raised", [
    (TEST_FILE_LIST[0], True, False),
    (TEST_FILE_LIST[3], True, True),
    (TEST_FILE_LIST[0], False, True),
])
def test_basefile_clear_file(env_setup_for_file_object,
                             create_filepath,
                             file_path,
                             exception_raised):
    my_file = BaseFile(file_path)
    if create_filepath:
        my_file.create_filepath()

    was_exception_raised = False
    try:
        my_file.clear_file()
    except FileNotFoundError:
        was_exception_raised = True
    except IsADirectoryError:
        was_exception_raised = True

    assert was_exception_raised == exception_raised


def test_basefile_clear_file_doesnt_create_file(tmp_path):
    my_file = BaseFile(path.join(tmp_path, 'testing.txt'))
    try:
        my_file.clear_file()
    except FileNotFoundError:
        pass
    except IsADirectoryError:
        pass
    assert not my_file.filepath_exists()


def test_basefile_get_contents_of_text_file(text_file):
    assert text_file.get_contents_of_file() == '0123456789'


def test_basefile_str(base_file):
    assert base_file.get_filepath() == str(base_file)


def test_encryptionfile_encrypt_and_decrypt(encryption_file):
    encryption_file.append_text_to_file("\nI am the second line.")
    contents_before_encryption = encryption_file.get_contents_of_file()
    encryption_file.encrypt()
    assert encryption_file.is_binary()
    encryption_file.decrypt()
    contents_after_encryption = encryption_file.get_contents_of_file()
    assert not encryption_file.is_binary()
    assert contents_before_encryption == contents_after_encryption


def test_large_encryption_file(large_txt_file, rsa_file):
    encryption_file = EncryptionFile(large_txt_file, rsa_file)
    contents_before_encryption = encryption_file.get_contents_of_file()
    encryption_file.encrypt()
    assert encryption_file.is_binary()
    encryption_file.decrypt()
    contents_after_encryption = encryption_file.get_contents_of_file()
    assert not encryption_file.is_binary()
    assert contents_before_encryption == contents_after_encryption


def test_encryptionfile_accepts_file_object_as_arguments(base_file, rsa_file):
    try:
        EncryptionFile(base_file, rsa_file)
    except TypeError:
        fail("Failed -- TypeError -- on \
             test_encryptionfile_accepts_file_object_as_arguments.")


def test_rsafile_gen_pem_file(rsa_file):
    assert rsa_file.filepath_exists()


def test_rsafile_get_key(rsa_file):
    assert rsa_file.get_key()


def test_text_file_init(text_file):
    assert text_file.filepath_exists()
    assert text_file.get_contents_of_file() == "0123456789"
