import sys
from os import path, chdir
from pytest import fixture, mark, fail
from random import choice
from string import ascii_uppercase

PARENT_DIR = path.abspath(path.join(path.dirname(__file__), path.pardir))

sys.path.append(PARENT_DIR)

from fileflamingo.BaseFile import BaseFile              # noqa: E402
from fileflamingo.RSAFile import RSAFile                # noqa: E402
from fileflamingo.EncryptionFile import EncryptionFile  # noqa: E402
from fileflamingo.TextFile import TextFile              # noqa: E402
from fileflamingo.Encryptor import Encryptor            # noqa: E402


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

CONTENTS_OF_TEXT_FILE = "USERNAME=JGRUGRU\nPASSWORD=12341515134$@#$^"

ENCRYPT_CHAR_LIMIT = 245


def create_file(fileclass, filepath, *args, **kwargs):
    my_file = fileclass(filepath, *args, **kwargs)
    my_file.create_filepath()
    return my_file


def str_factory(str_size):
    return ''.join(choice(ascii_uppercase) for i in range(str_size))


def encrypted_bytes_generator(encryptor, str_to_encrypt):
    return encryptor.encrypt_data(str_to_encrypt)


@fixture
def base_file(tmp_path):
    my_file = create_file(BaseFile, path.join(tmp_path, 'test.txt'))
    return my_file


@fixture
def text_file(tmp_path):
    my_file = create_file(
        TextFile,
        path.join(tmp_path, 'test.txt'),
        txt=CONTENTS_OF_TEXT_FILE)
    return my_file


@fixture
def rsa_file(tmp_path):
    my_rsa_file = create_file(RSAFile, path.join(tmp_path, 'my_key.pem'))
    my_rsa_file.gen_pem_file()
    return my_rsa_file


@fixture
def encryptor(rsa_file):
    return Encryptor(rsa_file)


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
                    'test_env.txt')))


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
    except (FileNotFoundError, IsADirectoryError):
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
    except (FileNotFoundError, IsADirectoryError):
        was_exception_raised = True

    assert was_exception_raised == exception_raised


def test_basefile_clear_file_doesnt_create_file(tmp_path):
    my_file = BaseFile(path.join(tmp_path, 'testing.txt'))
    try:
        my_file.clear_file()
    except (FileNotFoundError, IsADirectoryError):
        pass
    assert not my_file.filepath_exists()


def test_basefile_get_contents_of_text_file(text_file):
    assert text_file.get_contents_of_file() == CONTENTS_OF_TEXT_FILE


def test_basefile_str(base_file):
    assert base_file.get_filepath() == str(base_file)


@mark.parametrize("str_to_encrypt, exception_raised", [
    (str_factory(ENCRYPT_CHAR_LIMIT), False),  # why is this the limit?
    ("USERNAME=" + str_factory(236), False),
    ("PASSWORD=" + "aJh@WDFWDg-#4jZr" + str_factory(100), False),
    ("TESTING=" + "aJh@WDFWDg-#4jZr" + str_factory(250), True),
])
def test_encryptor_encrypt_and_decrypt_data(encryptor,
                                            str_to_encrypt,
                                            exception_raised):
    was_exception_raised = False
    try:
        data = encryptor.encrypt_data(str_to_encrypt)
    except ValueError:
        was_exception_raised = True
    if not was_exception_raised:
        assert isinstance(data, bytes)
    assert was_exception_raised == exception_raised


@mark.parametrize("original_str, is_decryptable", [
    (str_factory(ENCRYPT_CHAR_LIMIT), False),
    (str_factory(ENCRYPT_CHAR_LIMIT), True),
    (str_factory(140), True),
    (str_factory(1), True),
    ('0', True),
    ("aJh@WDFWDg-#4jZr", True),
])
def test_encryptor_decrypt_and_decrypt_data(encryptor,
                                            original_str,
                                            is_decryptable):
    if is_decryptable:
        str_to_decrypt = encrypted_bytes_generator(encryptor, original_str)
    else:
        str_to_decrypt = str.encode(original_str)
    was_exception_raised = False
    try:
        data = encryptor.decrypt_data(str_to_decrypt)
    except ValueError:
        was_exception_raised = True
    if not was_exception_raised:
        assert data == original_str
    assert was_exception_raised != is_decryptable


@mark.parametrize("str_to_encrypt, exception_raised", [
    (str_factory(ENCRYPT_CHAR_LIMIT)
        + '\n' + str_factory(ENCRYPT_CHAR_LIMIT)
        + '\n' + str_factory(ENCRYPT_CHAR_LIMIT), False),
    (str_factory(140), False),
    (str_factory(1), False),
    ('0', False),
    (str_factory(100) + "aJh@WDFWDg-#4jZr" + str_factory(10)
        + '\n' + str_factory(ENCRYPT_CHAR_LIMIT)
        + '\n' + str_factory(ENCRYPT_CHAR_LIMIT), False),
    (open(path.abspath(
        path.join(PARENT_DIR, 'tests/test_env.txt')), "r").read(), False),
])
def test_encryptionfile_encrypt_decrypt_file(tmp_path,
                                             rsa_file,
                                             str_to_encrypt,
                                             exception_raised):
    txt_file = create_file(
        TextFile,
        path.join(tmp_path, 'test.txt'),
        txt=str_to_encrypt)
    encryption_file = create_file(
        EncryptionFile,
        txt_file,
        rsa_file)
    encryption_file.encrypt()
    assert encryption_file.is_binary()
    encryption_file.decrypt()
    contents_after_encryption = encryption_file.get_contents_of_file()
    assert not encryption_file.is_binary()
    assert str_to_encrypt == contents_after_encryption


@mark.parametrize("random_bytes, exception_raised", [
    (str_factory(ENCRYPT_CHAR_LIMIT), True),
    (str.encode(str_factory(140)), False),
    (str.encode(str_factory(ENCRYPT_CHAR_LIMIT * 3)), False),
    (b"aJh@WDFWDg-#4jZr", False),
])
def test_encryptionfile_write_and_get_bytes(encryption_file,
                                            random_bytes,
                                            exception_raised):
    encryption_file.clear_file()
    was_exception_raised = False
    try:
        encryption_file.write_bytes_to_file(random_bytes)
    except TypeError:
        was_exception_raised = True

    if not was_exception_raised:
        assert random_bytes == encryption_file.get_bytes_from_file()

    assert was_exception_raised == exception_raised


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
    assert text_file.get_contents_of_file() == CONTENTS_OF_TEXT_FILE
