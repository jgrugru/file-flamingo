import sys
from os import path, chdir
from pytest import fixture, mark, fail

sys.path.append(path.abspath(path.join(path.dirname(__file__),
                path.pardir)))

from fileflamingo.BaseFile import BaseFile              # noqa: E402
from fileflamingo.RSAFile import RSAFile                # noqa: E402
from fileflamingo.EncryptionFile import EncryptionFile  # noqa: E402


@fixture
def base_file(tmp_path):
    my_file = create_file(path.join(tmp_path, 'env', '.env'))
    return my_file


@fixture
def base_file_with_content(base_file):
    base_file.append_text_to_file("0123456789")
    return base_file


@fixture
def env_setup_for_file_object(tmp_path):
    chdir(tmp_path)


@fixture
def rsa_file(tmp_path):
    my_rsa_file = RSAFile(path.join(tmp_path, 'my_key.pem'))
    my_rsa_file.gen_pem_file()
    return my_rsa_file


@fixture
def encryption_file(base_file_with_content, rsa_file):
    my_encrypytion_file = EncryptionFile(
        base_file_with_content,
        rsa_file.get_filepath())
    return my_encrypytion_file


@fixture
def large_txt_file():
    return BaseFile(path.abspath(path.join(path.dirname(__file__),
                    'test.txt')))


def create_file(filepath):
    my_file = BaseFile(filepath)
    my_file.create_filepath()
    return my_file


@mark.parametrize("file_path, is_file", [
    ("env_path/.env", True),
    ("./env_path/env", True),
    (".env_path/env", True),
    ("env_path/env/", False),
    (".env_path/env/", False),
    ("././././env/", False),
    ("././././env", True),
    ("../env_path/.env", True),
    ("../env_path1/.env/", False),
])
def test_basefile_create_filepath(env_setup_for_file_object,
                                  file_path,
                                  is_file):
    my_file = create_file(file_path)
    assert my_file.filepath_exists()
    assert my_file.is_file() == is_file


@mark.parametrize("file_path, exception_raised", [
    ("env_path/.env", False),
    ("./env_path/env", False),
    (".env_path/env", False),
    ("env_path/env/", True),
    (".env_path/env/", True),
    ("././././env/", True),
    ("././././env", False),
    ("../env_path/.env", False),
    ("../env_path1/.env/", True),
])
def test_basefile_delete_filepath(env_setup_for_file_object,
                                  file_path,
                                  exception_raised):
    my_file = create_file(file_path)

    was_exception_raised = False
    try:
        my_file.delete_file()
    except FileNotFoundError:
        was_exception_raised = True
    except IsADirectoryError:
        was_exception_raised = True

    assert was_exception_raised == exception_raised


@mark.parametrize("file_path, create_filepath, exception_raised", [
    ("env_path/.env", True, False),
    ("env_path/.env/", True, True),
    ("env_path/.env", False, True),
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


def test_basefile_get_contents_of_text_file(base_file_with_content):
    assert base_file_with_content.get_contents_of_file() == '0123456789'


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

# setup tests for individual functions. Need more testing.
# setup Mark.parametrize for encrypt and decrypt functions.
